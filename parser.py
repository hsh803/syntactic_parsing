"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
import sys
from sys import stdin, stderr
from time import time
from json import dumps

from collections import defaultdict
from pprint import pprint

from pcfg import PCFG
from tokenizer import PennTreebankTokenizer

def argmax(lst):
    return max(lst) if lst else (0.0, None)

def backtrace(back, bp):
    # ADD YOUR CODE HERE
    # Extract the tree from the backpointer
    #tree = []
    if len(back) == 4:
        return [back[2], back[3]] 
    elif len(back) == 6:
        tree = [back[3], backtrace(bp[back[0], back[1], back[4]], bp), backtrace(bp[back[1], back[2], back[5]], bp)] 
    return tree
    
    #return tree
    # https://github.com/RobMcH/CYK-Parser/blob/master/cyk_parser.py
def CKY(pcfg, norm_words):
    # ADD YOUR CODE HERE
    # IMPLEMENT CKY
    # NOTE: norm_words is a list of pairs (norm, word), where word is the word 
    #       occurring in the input sentence and norm is either the same word, 
    #       if it is a known word according to the grammar, or the string _RARE_. 
    #       Thus, norm should be used for grammar lookup but word should be used 
    #       in the output tree.

    # Initialize your charts (for scores and backpointers)
    n = len(norm_words)
    chart = defaultdict(float)
    bp = defaultdict(tuple)
    # Code for adding the words to the chart
    for i, (norm, word) in enumerate(norm_words):
        for rule in pcfg.q1:
            if norm == rule[1]:
                chart[(i, i+1, rule[0])] = pcfg.q1[rule]
                bp[(i, i+1, rule[0])] = (i, i+1, rule[0], word)
    # Code for the dynamic programming part, where larger and larger subtrees are built
    for mx in range(2, len(norm_words)+1):
        for mn in range(mx-2, -1, -1):
            for root in pcfg.N:
                best = 0
                best_bp = ()
                #print("mx, mn, root :", mx, mn, root)
                #print("Root, Binary: ", root,  pcfg.binary_rules[root])
                for rule in pcfg.binary_rules[root]:
                        #print("mx, mn, root :", mx, mn, root, rule)
                    for md in range(mn+1, mx):
                        t1 = chart[(mn, md, rule[0])]
                        t2 = chart[(md, mx, rule[1])]
                        candidate = t1 * t2 * pcfg.q2[(root, rule[0], rule[1])]
                        if candidate > best:
                            best = candidate
                            best_bp = (mn, md, mx, root, rule[0], rule[1])
                chart[mn, mx, root] = best
                bp[mn, mx, root] = best_bp
    # Below is one option for retrieving the best trees, assuming we only want trees with the "S" category
    # This is a simplification, since not all sentences are of the category "S"
    # The exact arguments also depends on how you implement your back-pointer chart.
    # Below it is also assumed that it is called "bp"
    return backtrace(bp[0, n, "S"], bp) 

class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()

    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:                # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = CKY(self.pcfg, norm_words)
        tree[0] = tree[0].split("|")[0]
        return tree

def display_tree(tree):
    pprint(tree)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python3 parser.py GRAMMAR")
        exit()

    start = time()
    grammar_file = sys.argv[1]
    print("Loading grammar from " + grammar_file + " ...", file=stderr)    
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)
    
    print("Parsing sentences ...", file=stderr)
    for sentence in stdin:
        tree = parser.parse(sentence)
        print(dumps(tree))
    print("Time: (%.2f)s\n" % (time() - start), file=stderr)

