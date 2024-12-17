class Tm:
    """
    a class for general turing machine
    """


    def __init__(self, tapes: list[list[any]],  states: set, currentState: str, deltaTable: dict, numOfTapes=1, acc = "acc", rej = "rej"):
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
        # initializes each tape with 2 spaces in the start and end of input
        self.tapes =  [['_', '_'] + tape + ['_', '_'] for tape in tapes]
        # if we got less tapes than the number of tapes in the machine, we initialize the missing tapes
        if len(tapes)< numOfTapes:
            for i in range(numOfTapes - len(tapes)+1):
                self.tapes.push(["_", "_", "_", "_"])
        
        self.states = states
        self.deltaTable = deltaTable
        self.currentState = currentState
        self.numOfTapes = numOfTapes
        self.acc, self.rej = acc, rej

        # initialize position of the head in each tape to be in index 2 (after the 2 spaces)
        self.pos = [2 for i in range(numOfTapes)] #[1, 3, 4]

    
    def __repr__(self):
        """
            string representation of the machine
        """
        return "\n".join(str(t) for t in self.tapes)


    def ensureBoundarySpace(self, tapeIndex: int, position: int):
        """
        adds spaces befre and after input if neccessary, and sets the position to the correct place

        params:
            - tapeIndex: the index of the tape in the tapes' list
            - position: in which position we need to add the space
        """
        # adds space before the input
        if position == -1:
            self.tapes[tapeIndex] = ["_"] + self.tapes[tapeIndex]
            self.pos[tapeIndex] = 0
        
        # adds space after the input
        tapeLength = len(self.tapes[tapeIndex])
        if position == tapeLength:
            self.tapes[tapeIndex] = self.tapes[tapeIndex] + ["_"] 
            self.pos[tapeIndex] = tapeLength

    def move (self, symbols: list):
        """
            params:
                - symbols: a list of the symbols that are in the head of each machine
            
            retrives the transition from the delta table and executes it

            for example:
                (q0, a, b, c): {newState: q1, write: [a, b, c], movement: [R, S, L] }

        """
      
        currentState = self.currentState
        # create a tuple from the current state and symbols to search the transition in the delta table
        deltaInput = (currentState,) + tuple(symbols)
        if deltaInput not in self.deltaTable:
            raise KeyError("the key {k} is not in the delta table".format(k=deltaInput))
        deltaOutput= self.deltaTable[deltaInput]
        
        newState, write, movements = deltaOutput["newState"], deltaOutput["write"], deltaOutput["movement"]

        # for each tape, in the head's position, write the symbol in the corresponding place in the list
        # write: [1, "_", 1], t: ["_", 1, 1, 1] (assume this is the second tape, i=1), self.pos: [4, 3, 1]
        # in the second tape, in index 3, we write "_" => t: ["_", 1, 1, "_"]
        
        for i, t in enumerate(self.tapes):
            t[self.pos[i]]= write[i]


        # move the head in each tape by the movements list from the delta table and ensure that the position isn't out of the tape's boundry,
        # 
        #  if it is - add a space and set the position to the correct place
        for i, m in enumerate(movements):
            if m == 'R':
                self.pos[i]+=1
                self.ensureBoundarySpace(i, self.pos[i])
            elif m == 'L':
                self.pos[i]-=1
                self.ensureBoundarySpace(i, self.pos[i])
        
        
        self.currentState = newState

   
    def config(self):
        """
        for each tape (i) prints a string of "uq sigma v", while:
            u= the left side of the head of tape i
            q = current state
            sigma = the symbol in the head of tape i
            v= the right side of the head in tape i
        """
        q = self.currentState
        config = "configuration: \n"
        for i, t in enumerate(self.tapes):
            p = self.pos[i]
            u, sigma, v = t[:p], t[p], t[p+1:]
            
            config += "tape {i}: {u} & {q} & {sig} & {v}  \n".format(i=i, u=u ,q=q ,sig=sigma ,v=v)
        print(config)

    
    def runMachine(self):
        """
            - runs the machine by the delta table as long as we didn't reach accept or reject
            - prints the starting configuration, and the configuration after each step
        """
        print("starting configuration:")
        self.config()
        while self.currentState != self.acc and self.currentState != self.rej:
            symbols = [t[self.pos[i]] for i, t in enumerate(self.tapes)]
            self.move(symbols)
            self.config()



    






