from src.programtree import Tree
import sys

if(len(sys.argv) > 2):
    print("provide only one file")
elif(len(sys.argv) == 0):
    print("please provide a file with the brainfuck program")

with open(sys.argv[1]) as f:
    Tree(f.read())
    