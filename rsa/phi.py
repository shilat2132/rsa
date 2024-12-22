from turingMachine import Tm
from basicMachines.mulMachine import mulPQ

def phiN(p: int, q: int):
    """
    - given prime numbers p and q, creates a machine with a tape for each one.
    - n = p*q
    - substracy 1 from each one and multiply them to get phi(n)
"""
    t1 = ["1" for i in range(p)]
    t2 = ["1" for i in range(q)]

    # create the delta table for subtracting 1 from each tape
    deltaTable = {
        # q0
        ("q0", "_", "1"): {"newState": "q0", "write": ["_", "1"], "movement": ["S", "R"] },
        ("q0", "1", "_"): {"newState": "q0", "write": ["1", "_"], "movement": ["R", "S"] },
        ("q0", "1", "1"): {"newState": "q0", "write": ["1", "1"], "movement": ["R", "R"] },
        ("q0", "_", "_"): {"newState": "sub", "write": ["_", "_"], "movement": ["L", "L"] },

        # sub
        ("sub", "1", "1"): {"newState": "acc", "write": ["_", "_"], "movement": ["S", "S"] }
    }

    states = {"q0", "sub"}
    subtractMachine = Tm([t1, t2], states, "q0", deltaTable, 2)
    subtractMachine.runMachine()
    print("the machine after substraction: \n{m}".format(m=subtractMachine))

    # create a multiplication machine with the tapes
    mul = mulPQ(subtractMachine.tapes)
    mul.runMachine()
    print("the machine after multiplication: \n{m}".format(m=mul))


