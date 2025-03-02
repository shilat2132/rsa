from tm import Tm
from utils import getLastCharIndex
from .addition import Addition

def complement(a: list):
    """
    gets a tape of a machine as an argument and changes it inplace to its Two's complement
    """

    deltaTable = {
         ("xor", 1) : {"newState": "xor", "write": [0], "movement": ['L']},
         ("xor", 0) : {"newState": "xor", "write": [1], "movement": ['L']},
         ("xor", "_") : {"newState": "add", "movement": ['S']},
    }

    pos = [getLastCharIndex(a)]
    currentState = "xor"

    while currentState != "acc":
        if currentState == "add":
            addMachine = Addition([a.copy(), [1], a])
            addMachine.runMachine()
            currentState = "acc"
        
        else:
            currentState = Tm.staticStep([a], currentState, deltaTable, pos)