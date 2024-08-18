from sys import stdin, stderr
from json import loads, dumps

def cnf(tree):
    # Assignment part to be completed by students
    n  = len(tree)
    if n == 2: 
        if n == 2 and isinstance(tree[1], list):
            #tree = [tree[0]+"+"+tree[1][0], *tree[1][1:]]
            new_label = [tree[0]+"+"+tree[1][0]]
            for i in tree[1][1:]:
                new_label.append(i)
            tree = new_label
            return cnf(tree)
        return tree
    elif n == 3 and isinstance(tree[1], list) and isinstance(tree[2], list):
        tree = [tree[0], cnf(tree[1]), cnf(tree[2])]
        return tree
    elif n > 3:
        #tree = tree[0], tree[1], [tree[0]+"|"+tree[1][0], *tree[2][2:]]
        new_label = [tree[0]+"|"+tree[1][0]]       
        for i in tree[2:]:
            new_label.append(i)
        tree = [tree[0], tree[1], new_label]
        return cnf(tree)
    else:
        pass


def is_cnf(tree):
    n = len(tree)
    if n == 2:
        return isinstance(tree[1], str)
    elif n == 3:
        return is_cnf(tree[1]) and is_cnf(tree[2])
    else:
        return False 

def words(tree):
    if isinstance(tree, str):
        return [tree]
    else:
        ws = []
        for t in tree[1:]:
            ws = ws + words(t)
        return ws

if __name__ == "__main__":

    for line in stdin:
        tree = loads(line)
        sentence = words(tree)
        input = str(dumps(tree))
        conv_tree = cnf(tree)
        if is_cnf(conv_tree) and words(conv_tree) == sentence:
            print(dumps(conv_tree))
        else:
            #print(dumps(conv_tree), "***False")
            print("Something went wrong!", file=stderr)
            print("Sentence: " + " ".join(sentence), file=stderr)
            print("Input: " + input, file=stderr)
            print("Output: " + str(dumps(conv_tree)), file=stderr)
            exit()

