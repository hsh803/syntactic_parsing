# Syntactic parsing
- Assigments from Syntactic parsing course from Language Technology Mater's program, Uppsala university
- Methods and algorithms used in automatic syntactic analysis (both phrase structure analysis and dependency analysis)

## 1. PCFG parsing (Probabilistic context free grammar)
- Implement a PCFG parser using the CKY algorithm and evaluate it using treebank data

### Data
- Trees of sentences (Penn Treebank): train.dat
- starter codes of cnf.py and parser.py from S. Stymme

### Process
1. Chomsky Normal Form (CNF): Complete a cnf function for converting trees to CNF in cnf.py
(CKY algorithm only accepts grammars in CNF. Therefore need to convert trees into CNF.)
´´´
python3 cnf.py < train.dat > outfile.txt
´´´

2. Grammar extraxtion: Run pcfg.py to extract PCFG in treebanks (outfile.txt)
´´´
python3 pcfg.py outfile.txt grammar.txt
´´´

3. CKY parsing: Complete argmax, backtrace, CKY functions in parser.py that can use the grammar to analyze new sentences using the CKY algorithm.
