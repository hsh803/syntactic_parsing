import sys

SH = 0; RE = 1; RA = 2; LA = 3;

labels = ["nsubj", "csubj", "nsubjpass", "csubjpass", "dobj", "iobj", "ccomp", "xcomp", "nmod", "advcl", "advmod", "neg", "aux", "auxpass", "cop", "mark", "discourse", "vocative", "expl", "nummod", "acl", "amod", "appos", "det", "case", "compound", "mwe", "goeswith", "name", "foreign", "conj", "cc", "punct", "list", "parataxis", "remnant", "dislocated", "reparandum", "root", "dep", "nmod:npmod", "nmod:tmod", "nmod:poss", "acl:relcl", "cc:preconj", "compound:prt"]

def read_sentences():
    sentence = []
    sentences = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            sentences.append(sentence)
            sentence = []
        elif line[0] != "#":
            token = line.split("\t")
            sentence.append(token)
    return(sentences)

def attach_orphans(arcs, n):
    attached = []
    for (h, d, l) in arcs:
        attached.append(d)
    for i in range(1, n):
        if not i in attached:
            arcs.append((0, i, "root"))

def print_tab(arcs, words, tags):
    hs = {}
    ls = {}
    for (h, d, l) in arcs:
        hs[d] = h
        ls[d] = l
    for i in range(1, len(words)):
        print("\t".join([words[i], tags[i], str(hs[i]), ls[i]]))
    print()
        
def print_tree(root, arcs, words, indent):
    if root == 0:
        print(" ".join(words[1:]))
    children = [(root, i, l) for i in range(len(words)) for l in labels if (root, i, l) in arcs]
    for (h, d, l) in sorted(children):
        print(indent + l + "(" + words[h] + "_" + str(h) + ", " + words[d] + "_" + str(d) + ")")
        print_tree(d, arcs, words, indent + "  ")

def transition(trans, stack, buffer, arcs):
    if trans[0] == SH:
        stack.insert(0, buffer.pop(0))
    # add code for missing transitions: (RE, "_"), (RA, label), (LA, label)
    elif trans[0] == LA:
          arcs.append((buffer[0], stack.pop(0), trans[1]))
    elif trans[0] == RA:
        arcs.append((stack[0], buffer[0], trans[1]))
        stack.insert(0, buffer.pop(0))
    elif trans[0] == RE:
        stack.pop(0)	
    return stack, buffer, arcs

def oracle(stack, buffer, heads, labels):
    # add code for missing transitions: (RE, "_"), (RA, label), (LA, label)
    if buffer[0] == heads[stack[0]]:
        return (LA, labels[stack[0]])
    elif stack[0] == heads[buffer[0]]:
        return (RA, labels[buffer[0]])
    for k in stack:    
        if buffer[0] == heads[k] or k == heads[buffer[0]]:
            return (RE, "_")
    return (SH, "_")

def parse(sentence):
    sentence.insert(0, ("root", "_", "0", "_"))
    words = [sentence[i][0] for i in range(len(sentence))]
    tags = [sentence[i][1] for i in range(len(sentence))]
    heads = [int(sentence[i][2]) for i in range(len(sentence))]
    labels = [sentence[i][3] for i in range(len(sentence))]
    stack = [0]
    buffer = [x for x in range(1, len(words))]
    arcs = []
    while buffer:
        trans = oracle(stack, buffer, heads, labels)
        #print(stack, buffer, heads, labels)
        #print(trans)
        stack, buffer, arcs = transition(trans, stack, buffer, arcs)
        #print(stack, buffer, heads, arcs)
    attach_orphans(arcs, len(words))
    if tab_format:
        print_tab(arcs, words, tags)
    else:
        print_tree(0, arcs, words, "")

if __name__ == "__main__":
    tab_format = False
    if len(sys.argv) == 2 and sys.argv[1] == "tab":
        tab_format = True
    for sentence in read_sentences():
        parse(sentence)
