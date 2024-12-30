from tm import Tm

class mulMachine(Tm):
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

            # start -> acc
            ("start", "_", "_", "_") : {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', 'S', 'S']},
            ("start", "_", "1", "_") : {"newState": "acc", "write": ["_", "1", "_"], "movement": ['S', 'S', 'S']},
            ("start", "_", "-", "_") : {"newState": "acc", "write": ["_", "-", "_"], "movement": ['S', 'S', 'S']},

            ("start", "1", "_", "_") : {"newState": "acc", "write": ["1", "_", "_"], "movement": ['S', 'S', 'S']},
            ("start", "-", "_", "_") : {"newState": "acc", "write": ["-", "_", "_"], "movement": ['S', 'S', 'S']},

            # start -> start
            ("start", "-", "-", "_") : {"newState": "start", "write": [ "-", "-", "_"], "movement": ['R', 'R', 'S']},
            ("start", "1", "-", "_") : {"newState": "start", "write": [ "1", "-", "-"], "movement": ['S', 'R', 'R']},
            ("start", "-", "1", "_") : {"newState": "start", "write": [ "-", "1", "-"], "movement": ['R', 'S', 'R']},

            # start-> q1
            ("start", "1", "1", "_") : {"newState": "q1", "write": [ "1", "1", "1"], "movement": ['S', 'R', 'R']},

            # q1 -> q1
            ("q1", "1", "1", "_") : {"newState": "q1", "write": [ "1", "1", "1"], "movement": ['S', 'R', 'R']},

            # q1 -> back
            ("q1", "1", "_", "_") : {"newState": "back", "write": [ "1", "_", "_"], "movement": ['R', 'L', 'S']},

            # back -> back
            ("back", "1", "1", "_") : {"newState": "back", "write": [ "1", "1", "_"], "movement": ['S', 'L', 'S']},

            # back -> q1
            ("back", "1", "_", "_") : {"newState": "q1", "write": [ "1", "_", "_"], "movement": ['S', 'R', 'S']},
            ("back", "1", "-", "_") : {"newState": "q1", "write": [ "1", "-", "_"], "movement": ['S', 'R', 'S']},


            # back -> acc
            ("back", "_", "1", "_") : {"newState": "acc", "write": [ "_", "1", "_"], "movement": ['S', 'S', 'S']},


        }


        super().__init__(tapes, states, "start", deltaTable, 3)

    def result(self):
        return self.tapes[2]