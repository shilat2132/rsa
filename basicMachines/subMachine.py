from tm import Tm

def subMachine(a: list[str], b: list[str]):
    """
    gets a and b in 2 different tapes in unary base and store the subtraction in the first tape
    """

    """
        case 1: a and b are non-negative:
            - run until the end of the a tape and start crossing 1 to the left side respectively with b tape
            - if a> b then the 1s in b would run out and we accept (5-3)
            - if a<b then the 1s in a would run out and we mark '-' in a, then add 1s to the right side until finishing the 1s in b (3-5)

        case 2: a and b are negative:
            - run until the end of the a tape and start crossing 1 to the left side respectively with b tape
            - if we reached '-' only in b, then accept (-4 - (-2))
            - if we reached '-' in a and not yet in b, cross the '-' and start adding 1s in a tape respectively with b (-3-(-5))
        
        case 3 and 4: a is negative and b isn't or the opposite:
            - run until the end of a and adds the 1s from b to a (-3-4 or 3-(-4))
    """
    
    deltaTable = {
    
        # start -> acc
        ("start", "1", "_") : {"newState": "acc", "write": ["1", "_"], "movement": ['S', 'S']},
        ("start", "-", "_") : {"newState": "acc", "write": ["-", "_"], "movement": ['S', 'S']},
        ("start", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']},


        # start-> end1 (end1 handles cases 1 and 2)
        ("start", "-", "-") : {"newState": "end1", "write": ["-", "-"], "movement": ['R', 'R']},
        ("start", "_", "1") : {"newState": "end1", "write": ["_", "1"], "movement": ['R', 'S']},
        ("start", "1", "1") : {"newState": "end1", "write": ["1", "1"], "movement": ['R', 'S']},

        # end1 -> end1
        ("end1", "1", "1") : {"newState": "end1", "write": ["1", "1"], "movement": ['R', 'S']},

        # end1-> sub1
        ("end1", "_", "1") : {"newState": "sub1", "write": ["_", "1"], "movement": ['L', 'S']},

        # sub1 -> sub1
        ("sub1", "1", "1") : {"newState": "sub1", "write": ["_", "1"], "movement": ['L', 'R']},

        # sub1 -> acc
        ("sub1", "1", "_") : {"newState": "acc", "write": ["1", "_"], "movement": ['S', 'S']},
        ("sub1", "-", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']},
        ("sub1", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']},


        # sub1 -> add1
        ("sub1", "_", "1") : {"newState": "add1", "write": ["-", "1"], "movement": ['R', 'S']},
        ("sub1", "-", "1") : {"newState": "add1", "write": ["1", "1"], "movement": ['R', 'R']},
        
        # add1 -> add1
        ("add1", "_", "1") : {"newState": "add1", "write": ["1", "1"], "movement": ['R', 'R']},

        # add1 -> acc
        ("add1", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']},

        # case 3 and 4
        # start -> end3
        ("start", "-", "1") : {"newState": "end3", "write": ["-", "1"], "movement": ['R', 'S']},
        ("start", "1", "-") : {"newState": "end3", "write": ["1", "-"], "movement": ['R', 'R']},
        ("start", "_", "-") : {"newState": "end3", "write": ["_", "-"], "movement": ['R', 'R']},

        # end3 -> end3
        ("end3", "1", "1") : {"newState": "end3", "write": ["1", "1"], "movement": ['R', 'S']},

        # end3 -> add3
        ("end3", "_", "1") : {"newState": "add3", "write": ["1", "1"], "movement": ['R', 'R']},

        # add3 -> add3
        ("add3", "_", "1") : {"newState": "add3", "write": ["1", "1"], "movement": ['R', 'R']},

        # add3 -> acc
        ("add3", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', 'S']}



    }

    Tm.staticRunMachine([a, b], "start", deltaTable)