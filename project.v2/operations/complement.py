from tm2 import Tm
from utils2 import getHeadIndex
from .addition import Addition
import copy 

def complement(a: list):
    """
    gets a tape of a machine as an argument and changes it inplace to its Two's complement
        - returns the steps list of the machine
    """

    deltaTable = {
         ("xor", 1) : {"newState": "xor", "write": [0], "movement": ['R']},
         ("xor", 0) : {"newState": "xor", "write": [1], "movement": ['R']},
         ("xor", "_") : {"newState": "add", "movement": ['S']},
    }

    pos = [getHeadIndex(a)]
    currentState = "xor"

    steps = []
    while currentState != "acc":
        if currentState == "add":
            tapes = [a.copy(), [1], a]
            addMachine = Addition(tapes)  # Create the addMachine first

            subMachibeStep = {
                "action": "submachine",
                "tapes": copy.deepcopy(addMachine.tapes)
            }
            sts = addMachine.runMachine()
            subMachibeStep["steps"] = sts
            steps.append(subMachibeStep)

            # Add the updateTapeStep right after the subMachineStep is appended
            updateTapeStep = {
                "action": "updateTape",
                "tape_index": 0,
                "tape": a.copy()
            }
            steps.append(updateTapeStep)

            currentState = "acc"
        
        else:
            currentState, step = Tm.staticStep([a], currentState, deltaTable, pos)
            steps.append(step)

    return steps