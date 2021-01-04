"""converts the brainfuck input program to a stream of symbols"""
from enum import Enum

class Symbol(Enum):
    """Enumerates all brainfuck Symbols"""
    INCREASE = 1
    DECREASE = 2
    ADD = 3
    REMOVE = 4
    OUTPUT = 5
    INPUT = 6
    LOOP_START = 7
    LOOP_END = 8
    PROGRAM_START = 9
    PROGRAM_END = 10

class SymbolStream():
    """filters any comments/non-symbols and returns a symbol for each command"""
    symbol_dict = {">":Symbol.INCREASE, "<":Symbol.DECREASE, "+":Symbol.ADD, "-":Symbol.REMOVE, 
                   ".":Symbol.OUTPUT, ",":Symbol.INPUT, "[":Symbol.LOOP_START, "]":Symbol.LOOP_END}

    """Reads the brainfuck code as a strem of symbols"""
    def __init__(self, brainfuck_code):
        self.brainfuck_code = str(brainfuck_code)
        self.index = 0
        self.comment = ""

    def next(self):
        """returns the next brainfuck symbol"""
        symbol = None
        while symbol is None:
            if self.index == len(self.brainfuck_code):
                return Symbol.PROGRAM_END
            symbol = self.symbol_dict.get(self.brainfuck_code[self.index])
            self.index += 1

        return symbol
