import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from turingMachine import Tm # type: ignore


class subPQ(Tm):


    def __init__(self, tapes):

        states = {"start", "q1"}
        

        deltaTable = {
                    # start
                    ("start", "1", "1", "_"): {"newState": "start", "write": ['X', "X", '_'], "movement": ['R', 'R', 'S']},
                    ("start", "1", "_", "_"): {"newState": "q1", "write": ['1', "_", '_'], "movement": ['S', 'S', 'S']},
                    ("start", "_", "1", "_"): {"newState": "q1", "write": ['_', "1", '_'], "movement": ['S', 'S', 'S']},


                    # q1
                    ("q1", "1", "_", "_"): {"newState": "q1", "write": ['1', "_", '1'], "movement": ['R', 'S', 'R']},
                    ("q1", "_", "_", "_"): {"newState": "acc", "write": ['_', "_", '_'], "movement": ['S', 'S', 'S']},

                    ("q1", "_", "1", "_"): {"newState": "q1", "write": ['_', "1", '1'], "movement": ['S', 'R', 'R']},


        }

        super().__init__(tapes, states, "start", deltaTable, 3) 