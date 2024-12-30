import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from turingMachine import Tm


class remainderPQ(Tm):


    def __init__(self, tapes):

        states = {"start", "q1", "q2", "q3"}


        deltaTable = {
            # start
            ("start", "1", "1", "_"): {"newState": "start", "write": ['X', "1", '_'], "movement": ['R', 'R', 'S']},
            ("start", "1", "_", "_"): {"newState": "q1", "write": ["1", "_", "_"], "movement": ['L', 'L', 'S']},
            #("start", "_", "_", "_"): {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', 'S', 'S']},
            ("start", "_", "1", "_"): {"newState": "q2", "write": ["_", "1", "_"], "movement": ['L', 'S', 'S']},



            # q1
            ("q1", "X", "1", "_"): {"newState": "q3", "write": ['1*', "1", '_'], "movement": ['S', 'S', 'S']},



            # q2
            ("q2", "X", "1", "_"): {"newState": "q2", "write": ['X', "1", "1"], "movement": ['L', 'S', 'R']},
            ("q2", "1*", "1", "_"): {"newState": "acc", "write": ["1*", "1", "_"], "movement": ['S', 'S', 'S']},
            
            # q3

            ("q3", "1*", "_", "_"): {"newState": "start", "write": ['1*', "_", '_'], "movement": ['R', 'R', 'S']},
            ("q3", "1*", "1", "_"): {"newState": "q3", "write": ['1*', "1", '_'], "movement": ['S', 'L', 'S']},

            

        }


        super().__init__(tapes, states, "start", deltaTable, 3)    