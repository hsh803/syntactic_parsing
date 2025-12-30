# Syntactic parsing
- Assigments from Syntactic parsing course from Language Technology Mater's program, Uppsala university
- Methods and algorithms used in automatic syntactic analysis (both phrase structure analysis and dependency analysis)

## 1. PCFG parsing (Probabilistic context free grammar)
- Implement a PCFG parser using the CKY algorithm and evaluate it using treebank data
- Reach F-score at least 75%

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

### Result
- Time for parsing is 11466.71s, F1-score is 0,726 (73%)


## 2. Denpendency parsing algorithm
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

## 3. CrossLingual Dependency Parsing
- Try out cross-lingual parsing by using UUParser to see how parsing for a low-resource language can be aided by using data from another language.
- Choose a target language to parse and two other transfer languages to be trained for parsing the target language.

### Data 
- UD treebank (Universal Dependencies): UD_Korean-GSD, UD_Turkish-Atis, UD_English-Atis
- Recommanded to choose treebanks in similar domain.
- Treebank files should be named by ISO id (the short name for each treebank, i.e. ko_gsd, sv_lines or en_ewt)

### Process
- Collect treebanks for three choosen language
: A target language treebank (TGT: Korean), A transfer language treebank that you believe will be good (GTRF: Turkish), A transfer language treebank that you do not believe will be good or at least not as good as GTRF (BTRF: English)

- Train the parser with single language, mutiple languages (UUParser)
: Install uuparser (https://github.com/UppsalaNLP/uuparser/blob/master/README.md)
: Make sure to use the same name convention given UD treebank when running following uuparser commands (ex. UD_Korean_GSD, UD_Turkish-Atis, UD_English-Atis)
: Make sure to use quotes around the treebanks when you have more than one treebank 

1) Single language
```
uuparser --outdir [results directory ex. result_ko] --datadir [your directory containing UD directories ex. . (current dir)] --include [treebank to train on denoted by its ISO id ex. ko_gsd-ud-train.conllu] --disable-rlmost --json-isos [json file ex. ./ud2.13_iso.json]
```
2) Multiple languages
```
uuparser --outdir [results directory ex. result_ko_en] --datadir [your directory containing UD directories ex. . (current dir)] --disable-rlmost --include ["treebanks to train on denoted by their ISO id" ex. "ko_gsd tr_atis"] --multiling --json-isos [json file ex. ./ud2.13_iso.json][json file ex. ./ud2.13_iso.json]
```

### Result(Best F1-scores of TGT, GTRF, BTRG in UAS/LAS)
- UAS: 42 (Korean), 46 (Korean-Turkish), 45 (Korean-English)
- LAS: 24 (Korean), 34 (Korean-Turkish), 32 (Korean-English)

## 4. Individual project
- Parsing Korean with MaltParser and UUParser
- Goal: How differently they work in operations, and how relatively good or bad they perform each other in parsing Korean, especially by comparing dependency relations and Pos-tagging of each parser.

### Data
- UD treebank (Universal Dependencies): UD_Korean-GSD (https://github.com/UniversalDependencies/UD_Korean-GSD/tree/master)
- Train: 4400, Test: 950 Korean sentences

### Process
1. Install parsers
- UUparser: https://github.com/UppsalaNLP/uuparser/blob/master/README.md
- Maltparser: https://www.maltparser.org/download.html

2. Prepare data
- Download and save train and test data of UD_Korean-GSD in the working directory
- Prepare coNLL-X files seperately by converting data in coNLL-U format to coNLL-x because MaltEval can only process data in coNLL-x format.
```
perl  /workdir/conllu_to_conllx.perl < input.conllu > output.conll
```

2. Train/Evaluate
- UUParser
: Train/Parse
```
uuparser --outdir . --datadir . --include ko_gsd
```
: Evaluate
- MaltParser
: Run
```
java -jar maltparser-1.9.2.jar
```
: Train/Parse
```
java -jar -Xmx2g maltparser-1.9.2.jar -c myparser -m learn -i marltparser_ko_train.conll
java -jar -Xmx2g maltparser-1.9.1.jar -c myparser -m parse -i maltparser_ko_dev.conll -o maltparser_output.conll
```
: Evaluate
```
java -jar -Xmx2g MaltEval.jar -g ../maltparser_ko_dev.conll -s ../maltparser_output.conll --GroupBy Deprel:all

--GroupBy Deprel:all
--GroupBy Cpostag:all
--Metric LAS;UAS
```

### Results
- Both scores of UUParser are slightly greater than those of MaltParser.
- The best LAS score is reached at epoch 29 in UUparser.
<img width="350" height="100" alt="image" src="https://github.com/user-attachments/assets/a482a6e1-ab96-4edf-ace2-fc60d2548c95" />
