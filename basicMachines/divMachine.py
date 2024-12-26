from turingMachine import Tm

class DivMachine(Tm):
    """
    a class that inherits from the Turing Machine's class
        - gets a and b in 2 different tapes in unary base and store the a//b in the third tape
    """
    def __init__(self, tapes):
        """
            initiates the multiplication tm fields and builds its delta table
        """
        states = {"q0", "back"}
        
        deltaTable = {
            # q0
            ("q0", "1", "1", "_"): {"newState": "q0", "write": ['1', "1", '_'], "movement": ['R', 'R', 'S']},
            
            ("q0", "_", "1", "_"): {"newState": "acc", "write": ['_', "1", '_'], "movement": ['S', 'S', 'S']},
            ("q0", "_", "_", "_"): {"newState": "acc", "write": ['_', "_", '_'], "movement": ['S', 'S', 'S']},
            
            ("q0", "1", "_", "_"): {"newState": "back", "write": ['1', "_", '1'], "movement": ['S', 'L', 'R']},
            ("q0", "_", "_", "_"): {"newState": "back", "write": ['_', "_", '1'], "movement": ['S', 'L', 'R']},

            # back
            ("back", '1', "1", '_'): {"newState": "back", "write": ['1', "1", '_'], "movement": ['S', 'L', 'S']},
            ("back", '_', "1", '_'): {"newState": "back", "write": ['_', "1", '_'], "movement": ['S', 'L', 'S']},

            ("back", '1', "_", '_'): {"newState": "q0", "write": ['1', "_", '_'], "movement": ['S', 'R', 'S']},
            ("back", '_', "_", '_'): {"newState": "q0", "write": ['_', "_", '_'], "movement": ['S', 'R', 'S']},
            
        
        }


        super().__init__(tapes, states, "q0", deltaTable, 3)