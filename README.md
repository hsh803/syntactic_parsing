# Syntactic parsing
- Assigments from Syntactic parsing course from Language Technology Mater's program, Uppsala university
- Methods and algorithms used in automatic syntactic analysis (both phrase structure analysis and dependency analysis)

## 1. PCFG parsing (Probabilistic context free grammar)
- Implement a PCFG parser using the CKY algorithm and evaluate it using treebank data
- Reach F-score at least 75%
- Results: Time for parsing is 11466.71s, F1-score is 0,726 (73%)

### Data (from S. Stymme)
- Trees of sentences (Penn Treebank): train.dat
- Raw sentences (spaced, seperated per line): dev.raw
- Tokenizer (Penn Treebank): tokenizer.py (used for dev.raw)
- Gold standard file for evaluation the parser: use dev.dat for converting it into CNF using cnf.py (completed version of cnf.py)
- Starter codes: cnf.py, parser.py
- Other implementing codes: pcfg.py, tokenizer.py, eval.py

### Process
1. Chomsky Normal Form (CNF): Complete a cnf function for converting trees to CNF in cnf.py
(CKY algorithm only accepts grammars in CNF. Therefore need to convert trees into CNF.)
```
python3 cnf.py < train.dat > outfile.txt
```

2. Grammar extraxtion: Run pcfg.py to extract PCFG in treebanks, CNF (outfile.txt)
```
python3 pcfg.py < outfile.txt > grammar.txt
```

3. CKY parsing: Complete argmax, backtrace, CKY functions in parser.py that can use the grammar to analyze new sentences using the CKY algorithm.
: tokenizer.py should be placed in same directory as parser.py
```
pythogn3 parser.py grammar.txt < dev.raw > tree.txt
```

4. Evaluation: Eveluate the accuracy of the parser using gold standard file
: Run python3 cnf.py < dev.dat > dev_cnf.txt
```
python3 eval.py dev_cnf.txt tree.txt
```

## 2. Denpendency parsing
- Implement som key components of a transition-based dependency parser and analyze its behavior.

### Data (from S. Stymme)
- Starter code: oracle.py
- Test code: en-ud-dev.tab
  
### Process
1. Transition system to build a dependency tree: Complete transition function where arc-eager transition system (Configurations: stack, buffer, arcs set, Transitions: move left/right arcs, shift, remove)
2. Oracle parser: Complete the oracle function to train the parser for predicting correct transitions and configurations given dependency tree.
3. Test the oracle parser: Run the parser on the development set (en-ud-dev.tab > result.out from the English UD treebank) and make dependency tree.
: Compare the original tree (en-ud-dev.tab vs. result.out)
```
python3 oracle.py tab < en-ud-dev.tab > result.out
```
