"""Converts a brainfuck symbol stream to a program tree"""
from symbol import Symbol, SymbolStream
from enum import Enum

class Action(Enum):
    ADD = 1
    PNTR_ADD = 2
    LOOP = 3
    OUTPUT = 4
    INPUT = 5
    PROGRAM_ROOT = 6

class TreeNode:
    def __init__(self, action, parent=None, value=0):
        self.action = action

        self.children = []
        self.parent = parent
        self.value = value
        self.visitcount = 0

    def append_child(self, child):
        self.children += [child]

    def remove_child(self, index):
        del self.children[index]

class Tree:
    """class implementing a program tree for brainfuck"""
    def __init__(self, stream):
        self.root = TreeNode(Action.PROGRAM_ROOT)
        self.current_node = self.root
        self.build_tree(stream)

    def tree_builder(self, symbol):
        """builds the program tree by interpreting the symbols as one of 5 actions"""
        if symbol == Symbol.INCREASE:
            node = TreeNode(Action.PNTR_ADD, parent=self.current_node, value=1)
            self.current_node.append_child(node)
        elif symbol == Symbol.DECREASE:
            node = TreeNode(Action.PNTR_ADD, parent=self.current_node, value=-1)
            self.current_node.append_child(node)
        elif symbol == Symbol.ADD:
            node = TreeNode(Action.ADD, parent=self.current_node, value=1)
            self.current_node.append_child(node)
        elif symbol == Symbol.REMOVE:
            node = TreeNode(Action.ADD, parent=self.current_node, value=-1)
            self.current_node.append_child(node)
        elif symbol == Symbol.LOOP_START:
            node = TreeNode(Action.LOOP, parent=self.current_node)
            self.current_node.append_child(node)
            self.current_node = node
        elif symbol == Symbol.LOOP_END:
            if self.current_node.parent is None:
                raise SyntaxError("Loop ends without start")
            self.current_node = self.current_node.parent
        elif symbol == Symbol.INPUT:
            node = TreeNode(Action.INPUT, parent=self.current_node)
            self.current_node.append_child(node)
        elif symbol == Symbol.OUTPUT:
            node = TreeNode(Action.OUTPUT, parent=self.current_node)
            self.current_node.append_child(node)

    def build_tree(self, stream):
        """creates the program tree from a symbol stream"""
        symbol = stream.next()
        while symbol != Symbol.PROGRAM_END:
            self.tree_builder(symbol)
            symbol = stream.next()

    def run_node(self, node, memory, pointer_index):
        """recursive execution of program node"""
        #padd 'memory list' if needed
        if pointer_index >= len(memory):
            memory += [0] * (pointer_index - len(memory) + 1)

        if node.action == Action.ADD:
            memory[pointer_index] += node.value
        elif node.action == Action.PNTR_ADD:
            pointer_index += node.value
        elif node.action == Action.OUTPUT:
            print(chr(memory[pointer_index]), end='')
        elif node.action == Action.INPUT:
            memory[pointer_index] = int(input())
        elif node.action == Action.LOOP:
            while memory[pointer_index] != 0:
                for child in node.children:
                    pointer_index = self.run_node(child, memory, pointer_index)
        elif node.action == Action.PROGRAM_ROOT:
            for child in node.children:
                pointer_index = self.run_node(child, memory, pointer_index)
        node.visitcount += 1
        return pointer_index

    def run_program(self):
        pointer_index = 0
        memory = []
        self.run_node(self.root, memory, pointer_index)


programtree = Tree(SymbolStream(input()))
programtree.run_program()