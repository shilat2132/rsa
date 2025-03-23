from tm import Tm
from utils import getHeadIndex
from basicMachines.mulMachine import mulMachine

def powerMachine(x: list, y: list):
    """
    a function for the machine x in the power of y
    returns: a tuple of (the tape of x in the power of y, the configuration)
    """
    tapes = [x, y, []]
    for i, t in enumerate(tapes):
        if len(t) == 0:
            tapes[i].append("_")

    
    pos = [getHeadIndex(t) for t in tapes]


    deltaTable = {
        # start
        ("start", "1", "_", "_") : {"newState": "acc", "write": ["1", "_", "1"], "movement": ['S', 'S', "S"]},
        ("start", "1", "1", "_") : {"newState": "q", "write": ["1", "1", "1"], "movement": ['S', 'S', "S"]},

        # q
        ("q", "1", "_", "1") : {"newState": "acc", "write": ["1", "_", "1"], "movement": ['S', 'S', "S"]},
        ("q", "1", "1", "1") : {"newState": "mul", "write": ["1", "1", "1"], "movement": ['S', 'S', "S"]},

        # mul
        ("mul", "1", "1", "1") : {"newState": "q", "write": ["1", "1", "1"], "movement": ['S', 'R', "S"]},
    }

    currentState = "start"
    # starting configuration
    config = Tm.config(tapes, currentState, pos) +"\n"

    # running the machine
    while currentState !="acc":
        if currentState =="mul":
            t2 = tapes[2].copy() #assign it to a new variable so we can send it as 2 tapes to the mulMachine
            Tm.emptyTape(tapes[2])
            m = mulMachine([tapes[0], t2, tapes[2]])
            config += m.runMachine()
            pos[2] = getHeadIndex(tapes[2])
        
        currentState = Tm.staticStep(tapes, currentState, deltaTable, pos)
        config+= Tm.config(tapes, currentState, pos)
    
    return tapes[2], config


   