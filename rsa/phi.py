from tm import Tm
from basicMachines.mulMachine import mulMachine

def phiN(tapes):
    """
    tapes: a list of 3 lists - the 2 first are p and q and the third one is the list in which the result would be stored
    - given prime numbers p and q in unary base, each one is a list - compute phi(n)
    - n = p*q
    - subtract 1 from each one and multiply them to get phi(n)
    
    returns: the configuration
"""

    tapes[0] = tapes[0].copy()
    tapes[1] = tapes[1].copy()
    # create the delta table for subtracting 1 from each tape
    deltaTable = {
        ("start", "1", "1", "_"): {"newState": "acc", "write": ["_", "_", "_"], "movement": ["S", "S", "S"] },
    }
    
    state, config = Tm.staticRunMachine(tapes, "start", deltaTable)

    phi = mulMachine(tapes)
    config+= phi.runMachine()
    return config


