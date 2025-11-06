<h1> ScrambleSeq: Generate and analyse scramble RNA or DNA sequences </h1>

<p> **ScrambleSeqAnalyzer** is a Python script designed to generate scrambled DNA or RNA sequences (permutations with the same base content) from an input sequence and evaluate their thermodynamic stability. The script uses the external command-line tool **RNAfold** (part of the ViennaRNA package) to calculate the minimum free energy ($\Delta G$) and the associated secondary structure. The goal is to identify the least stable scrambled sequences (those with the least negative or positive $\Delta G$). </p>

<h3> Packages and libraries </h3>

To run this script, the following must be installed and configured:

1.  **Python 3.x:**
2.  **ViennaRNA Package:** (the `RNAfold` command-line tool must be installed and accessible in the system's `PATH`)
3.  **Python Libraries:** pandas, tqdm

<h3> Usage </h3> 
python scrambleseq.py [-h] -t TYPE -s SEQUENCE [-n NSCRAMBLES] [-o OUTPUT]

<h4> Required Arguments </h4>
-t, --type Sequence type: DNA or RNA. (Required)
-s, --sequence Input DNA/RNA sequence (e.g., ATGC...). (Required)
<h4> Optional Arguments </h4>
-n, --nscrambles Number of unique scrambled sequences to generate and analyze. (Default = 1000)
-p, --paramters If DNA sequence, specify path for DNA parameters (Default = None)
-o, --output Output filename. (Default = "scrambled.dat")

<h3> Example </h3>
<h4> 500 RNA scrambled sequences from input </h4>
Bash
<code> python scrambleseq.py -t RNA -s "AUGCCAUGCUACGUAGCUAGCUAGCAU" -n 500 </code>
<h4> 2000 DNA scrambled sequences, output file and parameters specified </h4>
Bash
<code> python scrambleseq.py -t DNA -s "ATGCATGCATGCATGCATGCATGC" -n 2000 -p /home/user/miniconda3/envs/vienna/share/ViennaRNA/dna_mathews2004.par -o dna_scrambles.dat </code>
