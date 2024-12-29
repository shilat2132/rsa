from tm import Tm


class divMachine(Tm):
    """
    a class that inherits from the Turing Machine's class
        - gets a and b in 2 different tapes in unary base and store the divison in the third tape
    """
    def __init__(self, tapes):
        """
            initiates the division tm fields and builds its delta table
        """
        states = {"start", "div", "back"}
        
        deltaTable = {
            # start -> div
            ("start", "-", "1", "_") : {"newState": "div", "write": ['-', "1", '-'], "movement": ['R', 'S', 'R']},
            ("start", "1", "-", "_"): {"newState": "div", "write": ['1', "-", '-'], "movement": ['S', 'R', 'R']},
            ("start", "-", "-", "_"): {"newState": "div", "write": ['-', "-", '_'], "movement": ['R', 'R', 'S']},
            ("start", "1", "1", "_"): {"newState": "div", "write": ['1', "1", '_'], "movement": ['R', 'R', 'S']},

             # start -> acc
            ("start", "-", "_", "_") : {"newState": "acc", "write": ['-', "_", '_'], "movement": ['S', 'S', 'S']},
            ("start", "1", "_", "_") : {"newState": "acc", "write": ['1', "_", '_'], "movement": ['S', 'S', 'S']},

            ("start", "_", "-", "_") : {"newState": "acc", "write": ['_', "-", '_'], "movement": ['S', 'S', 'S']},
            ("start", "_", "1", "_") : {"newState": "acc", "write": ['_', "1", '_'], "movement": ['S', 'S', 'S']},

            ("start", "_", "_", "_") : {"newState": "acc", "write": ['_', "_", '_'], "movement": ['S', 'S', 'S']},
            
            # div -> back
            ("div", "1", "_", "_"): {"newState": "back", "write": ["1", "_", "1"], "movement": ['S', 'L', 'R']},
            ("div", "_", "_", "_"): {"newState": "back", "write": ["_", "_", "1"], "movement": ['S', 'L', 'R']},

            # div -> acc
            ("div", "_", "1", "_"): {"newState": "acc", "write": ["_", "1", "_"], "movement": ['S', 'S', 'S']},

            # div -> div
            ("div", "1", "1", "_"): {"newState": "div", "write": ["1", "1", "_"], "movement": ['R', 'R', 'S']},

            # back -> back
            ("back", "1", "1", "_"): {"newState": "back", "write": ['1', "1", "_"], "movement": ['S', 'L', 'S']},

            # back -> acc
            ("back", "_", "1", "_"): {"newState": "acc", "write": ["_", "1", "_"], "movement": ['S', 'S', 'S']},

            # back -> div
            ("back", "1", "_", "_"): {"newState": "div", "write": ["1", "_", "_"], "movement": ['S', 'R', 'S']},
            ("back", "1", "-", "_"): {"newState": "div", "write": ["1", "-", "_"], "movement": ['S', 'R', 'S']},


            

        }


        super().__init__(tapes, states, "start", deltaTable, 3)
    
    def resultTape(self):
        return self.tapes[2]