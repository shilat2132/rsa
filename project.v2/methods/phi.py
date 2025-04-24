from operations.multiplication import Multiplication
from operations.subtraction import Subtraction
import copy


def phiN(tapes):
    """
    tapes: a list of 3 lists - the 2 first are p and q and the third one is the list in which the result would be stored
    - given prime numbers p and q in binary base, each one is a list - compute phi(n)
    - n = p*q
    - subtract 1 from each one and multiply them to get phi(n)
    - returns a list of steps that were taken to compute phi(n)
    """
    steps = []

    # Subtract 1 from p: p1 = p - 1
    p1 = []
    subMachine = Subtraction([tapes[0], [1], p1])
    subMachineStep = {
        "action": "submachine",
        "formula": "p - 1",
        "tapes": copy.deepcopy(subMachine.tapes)
    }
    sts = subMachine.runMachine()
    subMachineStep["steps"] = sts
    steps.append(subMachineStep)


    # Subtract 1 from q: q1 = q - 1
    q1 = []
    subMachine = Subtraction([tapes[1], [1], q1])
    subMachineStep = {
        "action": "submachine",
        "formula": "q - 1",
        "tapes": copy.deepcopy(subMachine.tapes)
    }
    sts = subMachine.runMachine()
    subMachineStep["steps"] = sts
    steps.append(subMachineStep)

  

    # Multiply p1 and q1: phi(n) = (p - 1) * (q - 1)
    mulMachine = Multiplication([q1, p1, tapes[2]])
    subMachineStep = {
        "action": "submachine",
        "formula": "(p - 1) * (q - 1)",
        "tapes": copy.deepcopy(mulMachine.tapes)
    }
    sts = mulMachine.runMachine()
    subMachineStep["steps"] = sts
    steps.append(subMachineStep)


    return steps









