import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from basicMachines.subMachine import subMachine
from tm import Tm


class remainderPQ(Tm):


    def __init__(self, tapes):

        states = {"start", "q1", "back", "remainder"}


        deltaTable = {
            # start -> acc
            ("start", "_", "_", "_"): {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', 'S', 'S']},
            ("start", "1", "_", "_"): {"newState": "acc", "write": ["1", "_", "_"], "movement": ['S', 'S', 'S']},
            # start
            ("start", "1", "1", "_"): {"newState": "start", "write": ['X', "1", '_'], "movement": ['R', 'R', 'S']},
            ("start", "1", "_", "_"): {"newState": "q1", "write": ["1", "_", "_"], "movement": ['L', 'L', 'S']},
            ("start", "_", "_", "_"): {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', 'S', 'S']},
            ("start", "_", "1", "_"): {"newState": "q2", "write": ["_", "1", "_"], "movement": ['L', 'S', 'S']},

            # start -> q1
            ("start", "1", "1", "_"): {"newState": "q1", "write": ["1*", "1", "_"], "movement": ['R', 'R', 'S']},

            # q1 -> acc
            ("q1", "_", "_", "_"): {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', 'S', 'S']},
            
            # q1 -> q1
            ("q1", "1", "1", "_"): {"newState": "q1", "write": ["1", "1", "_"], "movement": ['R', 'R', 'S']},

            # q1-> back
            ("q1", "1", "_", "_"): {"newState": "back", "write": ["1", "_", "_"], "movement": ['S', 'L', 'S']},

            # q1 -> remainder
            ("q1", "_", "1", "_"): {"newState": "remainder", "write": ["_", "1", "_"], "movement": ['L', 'S', 'S']},


            # back -> back
            ("back", "1", "1", "_"): {"newState": "back", "write": ["1", "1", "_"], "movement": ['S', 'L', 'S']},

            # back -> start
            ("back", "1", "_", "_"): {"newState": "start", "write": ["1", "_", "_"], "movement": ['S', 'R', 'S']},
            
            # remainder -> remainder
            ("remainder", "1", "1", "_"): {"newState": "remainder", "write": ["1", "1", "1"], "movement": ['L', 'S', 'R']},

            # remainder -> acc
            ("remainder", "1*", "1", "_"): {"newState": "acc", "write": ["1*", "1", "1"], "movement": ['S', 'S', 'S']}
           
            

        }


        super().__init__(tapes, states, "start", deltaTable, 3) 

    def runMachine(self):
        """
        Handles the tapes: removes negative sign from the first tape if present
        and performs the remainder calculation.
        """
    

        if self.tapes[0][self.pos[0]] == "-":
            self.pos[0]+=1

            super().runMachine() #a%b
            subMachine(self.tapes[1] , self.tapes[2])
            Tm.copyTape(self.tapes[1], self.tapes[2])
        
        else:
            super().runMachine() #a%b

        # # Removing negative sign from the first tape
        # if tape1.startswith("-"):
        #     tape1 = tape1[1:]  

        # # Update tapes and perform remainder calculation
        # self.tapes = [tape1, tape2, ""]

        # # Running the remainder machine using super
        # super().run(self.tapes)

        # # Access the result from the third tape
        # tape3 = self.tapes[2]

        # # Perform subtraction between the second tape and the result on the third tape
        # tapes_subtraction = [tape2, tape3, ""]
        # subMachine(tapes_subtraction[0], tapes_subtraction[1])

        # # Storing the result on the fourth tape
        # tape4 = tapes_subtraction[2]
        # self.tapes.append(tape4)  
        # return tape4

        