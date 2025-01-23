from tm import Tm
def binary(a: list):
    """
        this function accepts a tape of a number(a) with unary base and creates a tape of the binary representation
            - the function makes a copy of a and soesn't change the original list
        returns: a tuple of the tape of the binary representation and the configuration
    """
    deltaTable = {

        # even
        ("even", "x", "_") : {"newState": "even", "write": ["x", "_"], "movement": ['R', 'S']},
        ("even", "1", "_") : {"newState": "odd", "write": ["x", "_"], "movement": ['R', 'S']},
        ("even", "_", "_") : {"newState": "back", "write": ["_", "0"], "movement": ['L', 'L']},


        # odd
        ("odd", "x", "_") : {"newState": "odd", "write": ["x", "_"], "movement": ['R', 'S']},
        ("odd", "1", "_") : {"newState": "even", "write": ["1", "_"], "movement": ['R', 'S']},
        ("odd", "_", "_") : {"newState": "back", "write": ["_", "1"], "movement": ['L', 'L']},

        # back
        ("back", "1", "_") : {"newState": "back", "write": ["1", "_"], "movement": ['L', 'S']},
        ("back", "x", "_") : {"newState": "back", "write": ["x", "_"], "movement": ['L', 'S']},
        ("back", "_", "_") : {"newState": "end?", "write": ["_", "_"], "movement": ['R', 'S']},

        # end?
        ("end?", "x", "_") : {"newState": "end?", "write": ["x", "_"], "movement": ['R', 'S']},
        ("end?", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']},
        ("end?", "1", "_") : {"newState": "even", "write": ["1", "_"], "movement": ['S', 'S']},
    }

    tapes = [a.copy(), []]
    state, config = Tm.staticRunMachine(tapes, "even", deltaTable)
    return tapes[1], config