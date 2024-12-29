from tm import Tm
from basicMachines.mulMachine import mulPQ

def phiN(p: list[str], q: list[str]):
    """
    - given prime numbers p and q in unary base, each one is a list - compute phi(n)
    - n = p*q
    - subtract 1 from each one and multiply them to get phi(n)
"""


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

    Tm.staticRunMachine([p, q], "q0", deltaTable)

    phi = mulPQ([p, q])
    phi.runMachine()
    print("phi(n): \n{p}".format(p=phi.tapes[2]))


