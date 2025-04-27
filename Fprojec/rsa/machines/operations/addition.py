from tm2 import Tm
from utils2 import getLastCharIndex

class Addition(Tm):

    def __init__(self, tapes):

        deltaTable ={
            # q0 -> acc
             ("q0", "_", "_", "_") : {"newState": "acc", "movement": ['S', 'S', 'S']},

            # q0 -> q0
            ("q0", 0, 0, "_") : {"newState": "q0", "write": [0, 0, 0], "movement": ['L', 'L', 'L']},
            ("q0", 0, 1, "_") : {"newState": "q0", "write": [0, 1, 1], "movement": ['L', 'L', 'L']},
            ("q0", 1, 0, "_") : {"newState": "q0", "write": [1, 0, 1], "movement": ['L', 'L', 'L']},

            ("q0", 0, "_", "_") : {"newState": "q0", "write": [0, "_", 0], "movement": ['L', 'S', 'L']},
            ("q0", 1, "_", "_") : {"newState": "q0", "write": [1, "_", 1], "movement": ['L', 'S', 'L']},
        
            ("q0", "_", 0, "_") : {"newState": "q0", "write": ["_", 0, 0], "movement": ['S', 'L', 'L']},
            ("q0", "_", 1, "_") : {"newState": "q0", "write": ["_", 1, 1], "movement": ['S', 'L', 'L']},
        
        
            # q0 -> qCarry
            ("q0", 1, 1, "_") : {"newState": "qCarry", "write": [1, 1, 0], "movement": ['L', 'L', 'L']},

            # qCarry ->acc
            ("qCarry", "_", "_", "_") : {"newState": "acc", "write": ["_", "_", 1], "movement": ['S', 'S', 'S']},

            # qCarry -> qCarry
            ("qCarry", 1, 1, "_") : {"newState": "qCarry", "write": [1, 1, 1], "movement": ['L', 'L', 'L']},
            ("qCarry", 0, 1, "_") : {"newState": "qCarry", "write": [0, 1, 0], "movement": ['L', 'L', 'L']},
        
            ("qCarry", 1, 0, "_") : {"newState": "qCarry", "write": [1, 0, 0], "movement": ['L', 'L', 'L']},
            ("qCarry", 1, "_", "_") : {"newState": "qCarry", "write": [1, "_", 0], "movement": ['L', 'S', 'L']},
            ("qCarry", "_", 1, "_") : {"newState": "qCarry", "write": ["_", 1, 0], "movement": ['S', 'L', 'L']},
        
            # qCarry -> q0
            ("qCarry", 0, 0, "_") : {"newState": "q0", "write": [0, 0, 1], "movement": ['L', 'L', 'L']},
            ("qCarry", 0, "_", "_") : {"newState": "q0", "write": [0, "_", 1], "movement": ['L', 'S', 'L']},
            ("qCarry", "_", 0, "_") : {"newState": "q0", "write": ["_", 0, 1], "movement": ['S', 'L', 'L']},
        }

        tapes[0] = tapes[0].copy()
        tapes[1] = tapes[1].copy()
        
        pos = []
        i1, i2 = getLastCharIndex(tapes[0]), getLastCharIndex(tapes[1]) #start from the lsb of the numbers
        pos.append(i1)
        pos.append(i2)
        pos.append(0)

        if len(tapes)== 3:  # Ensure there are 3 tapes
            tapes[2].clear()
        super().__init__(tapes, "q0", deltaTable, 3, pos)