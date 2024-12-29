from tm import Tm

class mulPQ(Tm):
    """
    a class that inherits from the Turing Machine's class
        - gets p and q in 2 different tapes in unary base and store the multiplication in the third tape
    """
    def __init__(self, tapes):
        """
            initiates the multiplication tm fields and builds its delta table
        """
        states = {"start", "q1", "back"}
        
        deltaTable = {
            # start
            ("start", "1", "1", "_") : {"newState": "q1", "write": ['x', "1", '_'], "movement": ['R', 'S', 'S']},
            ("start", "_", "1", "_"): {"newState": "acc", "write": ['_', "1", '_'], "movement": ['S', 'S', 'S']},
            
            # q1
            ("q1", "_", "_", "_"): {"newState": "back", "write": ['_', "_", '_'], "movement": ['S', 'L', 'S']},
            ("q1", "1", "_", "_"): {"newState": "back", "write": ['1', "_", '_'], "movement": ['S', 'L', 'S']},

            ("q1", "_", "1", "_"): {"newState": "q1", "write": ['_', "1", "1"], "movement": ['S', 'R', 'R']},
            ("q1", "1", "1", "_"): {"newState": "q1", "write": ["1", "1", "1"], "movement": ['S', 'R', 'R']},

            # back
            ("back", "_", "1", "_"): {"newState": "back", "write": ['_', "1", "_"], "movement": ['S', 'L', 'S']},
            ("back", "1", "1", "_"): {"newState": "back", "write": ["1", "1", "_"], "movement": ['S', 'L', 'S']},

            ("back", "_", "_", "_"): {"newState": "start", "write": ['_', "_", "_"], "movement": ['S', 'R', 'S']},
            ("back", "1", "_", "_"): {"newState": "start", "write": ["1", "_", "_"], "movement": ['S', 'R', 'S']}

        }


        super().__init__(tapes, states, "start", deltaTable, 3)