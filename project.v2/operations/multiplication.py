from tm import Tm
from .addition import Addition

class Multiplication(Tm):

    def __init__(self, tapes):

        states = {"start", "lsb", "checkCond", "add"}

        deltaTable = {
            # start -> acc
            ("start", "_", 1, "_") : {"newState": "acc", "movement": ['S', 'S', 'S']},
            ("start", "_", "_", "_") : {"newState": "acc", "movement": ['S', 'S', 'S']},
            ("start", 1, "_", "_") : {"newState": "acc", "movement": ['S', 'S', 'S']},

            # start -> lsb
            ("start", 1, 1, "_") : {"newState": "lsb", "movement": ['R', 'R', 'S']},

            # lsb -> lsb
            ("lsb", 1, 1, "_") : {"newState": "lsb", "movement": ['R', 'R', 'S']},
            ("lsb", 1, 0, "_") : {"newState": "lsb", "movement": ['R', 'R', 'S']},
            ("lsb", 0, 1, "_") : {"newState": "lsb", "movement": ['R', 'R', 'S']},
            ("lsb", 0, 0, "_") : {"newState": "lsb", "movement": ['R', 'R', 'S']},

            ("lsb", 1, "_", "_") : {"newState": "lsb", "movement": ['R', 'S', 'S']},
            ("lsb", 0, "_", "_") : {"newState": "lsb", "movement": ['R', 'S', 'S']},

            ("lsb", "_", 1, "_") : {"newState": "lsb", "movement": ['S', 'R', 'S']},
            ("lsb", "_", 0, "_") : {"newState": "lsb", "movement": ['S', 'R', 'S']},

            # lsb -> checkCond
            ("lsb", "_", "_", "_") : {"newState": "checkCond", "movement": ['S', 'L', 'S']},

            # checkCond -> checkCond
            ("checkCond", "_", 0, "_") : {"newState": "checkCond", "write": [0, 0, "_"], "movement": ['R', 'L', 'S']},
            ("checkCond", "_", 0, 0) : {"newState": "checkCond", "write": [0, 0, 0], "movement": ['R', 'L', 'S']},
            ("checkCond", "_", 0, 1) : {"newState": "checkCond", "write": [0, 0, 1], "movement": ['R', 'L', 'S']},

            # checkCond -> acc
            ("checkCond", "_", "_", "_") : {"newState": "acc", "movement": ['S', 'S', 'S']},
            ("checkCond", "_", "_", 0) : {"newState": "acc", "movement": ['S', 'S', 'S']},
            ("checkCond", "_", "_", 1) : {"newState": "acc", "movement": ['S', 'S', 'S']},

            # checkCond -> add
            ("checkCond", "_", 1, "_") : {"newState": "add", "movement": ['S', 'S', 'S']},
            ("checkCond", "_", 1, 0) : {"newState": "add", "movement": ['S', 'S', 'S']},
            ("checkCond", "_", 1, 1) : {"newState": "add", "movement": ['S', 'S', 'S']},

            # add -> checkCond
            ("add", "_", 1, "_") : {"newState": "checkCond", "write": [0, 1, "_"], "movement": ['R', 'L', 'S']},
            ("add", "_", 1, 0) : {"newState": "checkCond", "write": [0, 1, 0], "movement": ['R', 'L', 'S']},
            ("add", "_", 1, 1) : {"newState": "checkCond", "write": [0, 1, 1], "movement": ['R', 'L', 'S']}
        }
        super().__init__(tapes, states, "start", deltaTable, 3)

    
    def runMachine(self):
        # tapes = [a, b, y], compute: y = a*b
        while self.currentState != "acc":
            if self.currentState == "add":
                t = self.tapes[2].copy() # t= y
                Addition([t, self.tapes[0].copy(), self.tapes[2]]).runMachine() #y= a+y
            
            self.step()