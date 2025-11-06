import random
import subprocess
import os
import pandas as pd
from tqdm import tqdm # loading bar
import sys, argparse

# Calculate Delta G using RNAfold
def calculate_delta_g(sequence, parameters = None):
    """
    Parameters for DNA:
    --noconv : do not translate T into U
    -P : specify DNA parameters
    """
    try:
        if strand_type == "RNA":
            command = f"echo {sequence} | RNAfold"
            
        elif strand_type == "DNA":
            command = f"echo {sequence} | RNAfold --noconv -P {parameters}" 

        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.DEVNULL)
        
        lines = result.strip().split('\n')
        if len(lines) < 2:
            return None, None

        # Grep second line (structure and delta G)
        structure_line = lines[1].strip()

        # Extract delta G
        start_index = structure_line.rfind('(')
        end_index = structure_line.rfind(')')
        if start_index != -1 and end_index != -1:
            delta_g_str = structure_line[start_index + 1:end_index].strip()
            delta_g = float(delta_g_str)
            
            # Extract secondary structure
            structure = structure_line[:start_index].strip()
            
            return delta_g, structure 
        else:
            return None, None
            
    # Handling errors
    except FileNotFoundError:
        tqdm.write("\nERROR: 'RNAfold' not found. Check ViennaRNA is installed and loaded.")
        return None, None
    except Exception as e:
        return None, None


## Main script
parser = argparse.ArgumentParser(description="Create scrambled DNA/RNA sequences starting from an input sequence, and evaluate DeltaG energy using RNAfold\nRequires RNAfold installed and loaded!", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-t", "--type", help="Sequence type (DNA / RNA)" , required=True)
parser.add_argument("-s", "--sequence", help="Input DNA/RNA sequence" , required=True)
parser.add_argument("-n", "--nscrambles", help="Number of scramble sequences to generate", type = int, default = 1000)
parser.add_argument("-p", "--parameters", help = "DNA parameters", default = None)
parser.add_argument("-o", "--output", help="Output filename", default = "scrambled.dat")

# Initial data
args=parser.parse_args()

strand_type = args.type
input_seq = args.sequence
num_scrambles = args.nscrambles
parameters = args.parameters
output = args.output

if strand_type == "DNA" and not parameters:
    print("ERROR! Specify DNA parameters")
    exit()
if parameters:
    print(f"Using DNA parameters: {parameters}\n")

# Get bases content
list_of_bases = list(input_seq)
A = input_seq.count("A")
C = input_seq.count("C")
T = input_seq.count("T")
G = input_seq.count("G")
print(f"Input sequence: {input_seq}")
print(f"Base content: A = {A}, T = {T}, C = {C}, G = {G}\n")

scrambled_sequences = []
outfile = open(output, "w") 

print(f"Generating {num_scrambles} unique scramble sequences...")

# Define a set to memorize sequences and avoid evaluating the same sequence twice
analyzed_sequences_set = set()
unique_sequences_analyzed = 0 
sequences_generated_attempts = 0

# Iterate with tqdm until the number of unique sequences is analysed
with tqdm(total=num_scrambles, desc="Sequences") as pbar:
    while unique_sequences_analyzed < num_scrambles:
        
        # Generate scramble sequences
        shuffled_bases = random.sample(list_of_bases, len(list_of_bases))
        scrambled_dna = "".join(shuffled_bases)
        sequences_generated_attempts += 1
        
        # Check duplication and skip to next iteration
        if scrambled_dna in analyzed_sequences_set:
            continue
        
        # Add sequence to set
        analyzed_sequences_set.add(scrambled_dna)
        
        # Calculate delta G and secondary structure
        delta_g, structure = calculate_delta_g(scrambled_dna, parameters)
        if delta_g is not None:
            
            scrambled_sequences.append({
                "sequence": scrambled_dna,
                "delta_g": delta_g,
                "structure": structure
            })
            
            # Update count of unique sequences analyzed
            unique_sequences_analyzed += 1
            
            # Write in output file and standard output if Delta G >= 0
            if delta_g >= 0:
            # use tqdm to write in standard output to not interfere with loading bar
                tqdm.write(f"SEQUENCE (ΔG ≥ 0): {scrambled_dna}\tDelta G: {delta_g:.2f}\tStructure: {structure}")
                outfile.write(f"Sequence: {scrambled_dna}\tDelta G: {delta_g:.2f}\tStructure: {structure}\n")
            
            # Update loading bar
            pbar.update(1)
            success_rate = (unique_sequences_analyzed / sequences_generated_attempts) * 100 if sequences_generated_attempts > 0 else 0
            pbar.set_postfix_str(f"Analysed: {sequences_generated_attempts}, Unique: {success_rate:.2f}%")

# Close output file
outfile.close()

print(f"\nAnalysis complete. Total unique sequences analysed: {len(scrambled_sequences)}")
print(f"Total number of sequences generated: {sequences_generated_attempts}")

# Selection of least stable scramble sequences, ordered by Delta G
if not scrambled_sequences:
    print("No scramble sequence to select")
    exit()

df_all_results = pd.DataFrame(scrambled_sequences)
df_all_results_sorted = df_all_results.sort_values(by='delta_g', ascending=False)
df_final_best = df_all_results_sorted.head(10).copy() 

df_final_best.rename(columns={
    'sequence': 'Scramble sequence', 
    'delta_g': 'Delta G (kcal/mol)',
    'structure': 'Secondary structure'
}, inplace=True)

print("\n" + "#"*70)
print("FINAL RESULTS (top 10 sequences with ΔG ≥ 0)")
print("#"*70)

print(df_final_best[['Scramble sequence', 'Delta G (kcal/mol)', 'Secondary structure']])

print("\n" + "="*70)
print(f"Original sequence: {input_seq} (Length {len(input_seq)})")
print(f"Data written in: {output}")
print("="*70)

