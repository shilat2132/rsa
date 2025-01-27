
from utils import getHeadIndex, unaryToDecimal

class Tm:
    """
    A class for general Turing machine
    """

    def __init__(self, tapes: list[list[any]], states: set, currentState: str, deltaTable: dict, numOfTapes=1, acc="acc", rej="rej"):
        """
        a constructor for a turing machine
            params:
            - tapes: 2 dimensional list, where each element is a tape represented by a list
            - currentState: the state that the machine is currently on, initializes with the starting state.
            - deltaTabel: a dictonary of the transitions. each key is a tuple (currentState, the symbols in the head of each tape) 
                and the value is a dict of the new state, what to write and the movement
            
            other fields:
            - pos: a list of the position of each tape
            

        """
        
        for i, t in enumerate(tapes):
            if len(t) == 0:
                tapes[i].append('_')

        self.tapes = tapes

       # if we got less tapes than the number of tapes in the machine, we initialize the missing tapes
        if len(tapes) < numOfTapes:
            for i in range(numOfTapes - len(tapes)):
                self.tapes.append(["_", "_", "_", "_"])
        
        self.states = states
        self.deltaTable = deltaTable
        self.currentState = currentState
        self.numOfTapes = numOfTapes
        self.acc, self.rej = acc, rej
        
        # initialize position of the head in each tape to be the first character that's different from "_" or the first one 
            # if there's no character like that
        self.pos = [getHeadIndex(t) for t in self.tapes]


    @staticmethod
    def staticStep(tapes: list[list], currentState, deltaTable, pos):
        """
        a static method to simulate one step in the machine
            - internal method that adds spaces at the beginning or end of a tape if needed

            returns:
            the new current state 
        """

        def ensureBoundarySpace(tapeIndex: int, position: int):
            """
        adds spaces befre or after input if neccessary, and sets the position to the correct place

        params:
            - tapeIndex: the index of the tape in the tapes' list
            - position: in which position we need to add the space
        """
            if position == -1:
                tapes[tapeIndex].insert(0, "_")
                pos[tapeIndex] = 0
            
            tapeLength = len(tapes[tapeIndex])
            if position == tapeLength:
                tapes[tapeIndex].append("_")
                pos[tapeIndex] = tapeLength

        # create the symbols
        symbols = [t[pos[i]] for i, t in enumerate(tapes)]

        # create the input for the delta table and extract the transition from the table
        deltaInput = (currentState,) + tuple(symbols)
        if deltaInput not in deltaTable:
            raise KeyError(f"the key {deltaInput} is not in the delta table")
            
        deltaOutput = deltaTable[deltaInput]
        write = deltaOutput["write"] if "write" in deltaOutput else None
        newState, movements = deltaOutput["newState"], deltaOutput["movement"]

        # simulate writing in the tapes
        if write is not None:
            for i, t in enumerate(tapes):
                t[pos[i]] = write[i]

        # simulate moving according to the movement list
    
        for i, m in enumerate(movements):
            if m == 'R':
                pos[i] += 1
                ensureBoundarySpace(i, pos[i])
            elif m == 'L':
                pos[i] -= 1
                ensureBoundarySpace(i, pos[i])

        # return the new current state
        return newState

    @staticmethod
    def config(tapes: list[list], currentState, pos):
            """
            for each tape (i) presents a string of "uq sigma v", where:
                - u= the left side of the head of tape i
                - q = current state
                - sigma = the symbol in the head of tape i
                - v= the right side of the head in tape i
            
                returns: the string of the configuration
            """
            q = currentState
            config = "configuration: \n"
            for i, t in enumerate(tapes):
                p = pos[i]
                u, sigma, v = t[:p], t[p], t[p+1:]
                config += f"tape {i}: {u} & {q} & {sigma} & {v}  \n"
            return config

    @staticmethod
    def staticRunMachine(tapes: list[list], currentState, deltaTable: dict, pos: list[int] = None, acc= "acc", rej= "rej") -> str:
        """
        Static method to run the Turing machine based on the delta table.
        returns: a tuple of the last state and configuration for this run
        """
        
        # for empty tapes - initiates with spaces
        for i, t in enumerate(tapes):
            if len(t) == 0:
                tapes[i].append('_')

        if not pos:
            pos = [getHeadIndex(t) for t in tapes]

       
        config = Tm.config(tapes, currentState, pos) + "\n"
        
        while currentState != acc and currentState != rej:
            currentState = Tm.staticStep(tapes, currentState, deltaTable, pos)
            config+=Tm.config(tapes, currentState, pos) + "\n"
        
        return currentState, config

    @staticmethod
    def emptyTape(t: list[str]):
        """
        given a tape of the machine, erase all characters different from '_'
        returns: the configuration
        """

        deltaTable= {
            ("delete", "1") : {"newState": "delete", "write": ["_"], "movement": ['R']},
            ("delete", "-") : {"newState": "delete", "write": ["_"], "movement": ['R']},
            ("delete", "_") : {"newState": "acc", "write": ["_"], "movement": ['S']},
        }

        currentState, config =  Tm.staticRunMachine([t], "delete", deltaTable)
        return config


    @staticmethod
    def copyTape(a: list[str], b:list[str]):
        """
        given 2 tapes in a machine - copy tape a to tape b
        returns: the configuration string
        """

        deltaTable = {
            ("copy", "1", "1") : {"newState": "copy", "write": ["1", "1"], "movement": ['R', "R"]},
            ("copy", "1", "-") : {"newState": "copy", "write": ["1", "1"], "movement": ['R', "R"]},
            ("copy", "1", "_") : {"newState": "copy", "write": ["1", "1"], "movement": ['R', "R"]},

            ("copy", "-", "1") : {"newState": "copy", "write": ["-", "-"], "movement": ['R', "R"]},
            ("copy", "-", "-") : {"newState": "copy", "write": ["-", "-"], "movement": ['R', "R"]},
            ("copy", "-", "_") : {"newState": "copy", "write": ["-", "-"], "movement": ['R', "R"]},

            ("copy", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', "S"]},

            ("copy", "_", "1") : {"newState": "deleteRest", "write": ["_", "_"], "movement": ['S', "R"]},
            ("copy", "_", "-") : {"newState": "deleteRest", "write": ["_", "_"], "movement": ['S', "R"]},

            ("deleteRest", "_", "1") : {"newState": "deleteRest", "write": ["_", "_"], "movement": ['S', "R"]},
            ("deleteRest", "_", "-") : {"newState": "deleteRest", "write": ["_", "_"], "movement": ['S', "R"]},
            ("deleteRest", "_", "_") : {"newState": "acc", "write": ["_", "_"], "movement": ['S', "S"]},
        }

        currentState, config =  Tm.staticRunMachine([a, b], "copy", deltaTable)
        return config


    # instance methods
    def step(self):
        """
            Wrapper instance method that calls the static `staticStep` method.
            - updates the currentState after the transition
        """
        self.currentState = Tm.staticStep(self.tapes, self.currentState, self.deltaTable, self.pos)
    
    def runMachine(self):
        """
        Wrapper instance method that calls the static `staticRunMachine` method.
        returns: the configuration
        """
        self.currentState, config = Tm.staticRunMachine(self.tapes, self.currentState, self.deltaTable, self.pos)
        return config
    
   
    def trim_ones(t):
        # Find the last index where "1" appears
        try:
            last_one_index = len(t) - 1 - t[::-1].index("1")
            # Slice the list up to the last "1"
            t[:] = t[:last_one_index + 1]
        except ValueError:
            # If "1" is not in the list, return an empty list
            return



    def __repr__(self):
        """
            string representation of the machine
        """
        machine = ""
        for t in self.tapes:
            num = unaryToDecimal(t)
            machine += str(t) + ", the number in this tape: " + str(num) + "\n"
        return machine

