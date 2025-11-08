## ScrambleSeq: Generate and analyse scramble RNA or DNA sequences

**_ScrambleSeq_** is a Python script designed to generate scrambled DNA or RNA sequences (permutations with the same base content) from an input sequence and evaluate their thermodynamic stability. The script uses the external command-line tool **RNAfold** (part of the ViennaRNA package) [1] to calculate the minimum free energy ($\Delta G$) and the associated secondary structure. The goal is to identify the least stable scrambled sequences (those with the least negative or positive $\Delta G$).

### Requirements
To run this script, the following must be installed and configured:
1.  **Python 3.x:**
2.  **ViennaRNA Package:** (the `RNAfold` command-line tool must be installed and accessible in the system's `PATH`) [1]
3.  **Python Libraries:** pandas, tqdm

### Usage 
<code> python scrambleseq.py [-h] -t TYPE -s SEQUENCE [-n NSCRAMBLES] [-o OUTPUT] </code>

#### Required Arguments
-t, --type : Sequence type (DNA or RNA). (Required)  
-s, --sequence : Input DNA/RNA sequence (e.g., ATGC...). (Required)
#### Optional Arguments
-n, --nscrambles : Number of unique scrambled sequences to generate and analyze. (Default = 1000)  
-p, --paramters : If DNA sequence, specify path for DNA parameters (Default = None)  
-o, --output : Output filename. (Default = "scrambled.dat")

### Example
500 RNA scrambled sequences from input  
<code> python scrambleseq.py -t RNA -s "AUGCCAUGCUACGUAGCUAGCUAGCAU" -n 500 </code>  
2000 DNA scrambled sequences, output file and parameters specified  
<code> python scrambleseq.py -t DNA -s "ATGCATGCATGCATGCATGCATGC" -n 2000 -p /home/user/miniconda3/envs/vienna/share/ViennaRNA/dna_mathews2004.par -o dna_scrambles.dat </code>

#### References
[1] Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler, and Ivo L. Hofacker. ViennaRNA package 2.0. Algorithms for Molecular Biology, 6(1):26, 2011. doi:10.1186/1748-7188-6-26.
