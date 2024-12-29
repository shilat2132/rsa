
from utils import getHeadIndex

class Tm:
    """
    A class for general Turing machine
    """

    def __init__(self, tapes: list[list[any]], states: set, currentState: str, deltaTable: dict, numOfTapes=1, acc="acc", rej="rej"):
        """
        a constructor for a turing machine
            - tapes: 2 dimensional list, where each element is a tape represented by a list
            - states: a set of the states of the machine
            - currentState: the state that the machine is currently on, initializes with the starting state.
            - deltaTabel: a dictonary of the transitions. each key is a tuple (currentState, the symbols in the head of each tape) 
                and the value is a dict of the new state, what to write and the movement
            - numOfTapes: the number of tapes in the machine, defaulted to 1 tape
            - pos: a list of the position of each tape
            - acc: the name of the accepting state, defaulted to acc
            - rej: the name of the rejecting state, defaulted to rej

        """
        self.tapes = [['_', '_'] + tape + ['_', '_'] for tape in tapes]
       
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
    def staticRunMachine(tapes: list[list[any]], currentState: str, deltaTable: dict, acc= "acc", rej= "rej", pos: list[int] = None):
        """
        Static method to run the Turing machine based on the delta table.
        Includes internal methods `config`, `ensureBoundarySpace`, and `move`.
        """
        
        for i, t in enumerate(tapes):
            if len(t) == 0:
                tapes[i] = ['_', '_'] + t + ['_', '_']

        if not pos:
            pos = [getHeadIndex(t) for t in tapes]


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

        def config():
            """
            for each tape (i) prints a string of "uq sigma v", where:
                - u= the left side of the head of tape i
                - q = current state
                - sigma = the symbol in the head of tape i
                - v= the right side of the head in tape i
            """
            q = currentState
            config = "configuration: \n"
            for i, t in enumerate(tapes):
                p = pos[i]
                u, sigma, v = t[:p], t[p], t[p+1:]
                config += f"tape {i}: {u} & {q} & {sigma} & {v}  \n"
            print(config)

        def move(symbols: list):
            """
            Performs the movement and update the tapes based on the delta table.
                - symbols: the list of the characters in the head of each tape
            """
            nonlocal currentState
            deltaInput = (currentState,) + tuple(symbols)
            if deltaInput not in deltaTable:
                raise KeyError(f"the key {deltaInput} is not in the delta table")
            
            deltaOutput = deltaTable[deltaInput]
            newState, write, movements = deltaOutput["newState"], deltaOutput["write"], deltaOutput["movement"]

            # Write symbols to the tapes
            for i, t in enumerate(tapes):
                t[pos[i]] = write[i]

            # Move heads according to the movement list
            for i, m in enumerate(movements):
                if m == 'R':
                    pos[i] += 1
                    ensureBoundarySpace(i, pos[i])
                elif m == 'L':
                    pos[i] -= 1
                    ensureBoundarySpace(i, pos[i])

            currentState = newState

        # back to the runMachine method. 
        print("starting configuration:")
        config()
        
        while currentState != acc and currentState != rej:
            symbols = [t[pos[i]] for i, t in enumerate(tapes)]
            move(symbols)
            config()

    
    def runMachine(self):
        """
        Wrapper instance method that calls the static `staticRunMachine` method.
        """
        Tm.staticRunMachine(self.tapes, self.currentState, self.deltaTable, self.acc, self.rej, self.pos)

    
    def __repr__(self):
        """
            string representation of the machine
        """
        return "\n".join(str(t) for t in self.tapes)
