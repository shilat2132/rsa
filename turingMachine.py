class Tm:
    def __init__(self, tapes,  states, currentState, deltaTable, numOfTapes=1):
        self.tapes =  [['_', '_'] + tape + ['_', '_'] for tape in tapes]
        self.states = states
        self.deltaTable = deltaTable
        self.currentState = currentState
        self.numOfTapes = numOfTapes
        self.pos = [2 for i in range(numOfTapes)] #[1, 3, 4]

    
    def __repr__(self):
        for t in self.tapes:
            print(t)

    # state, mark, new state, write, movement
    def move (self, currentState, symbols):
        """
        {
        (q0, a, b, c): {newState: q1, write: [a, b, c], movement: [R, S, L] }
        }
        """
        deltaInput = (currentState,) + tuple(symbols)
        print("Type of deltaInput:", type(deltaInput))
        newDelta= self.deltaTable[deltaInput]
        
        write = newDelta["write"]
        movements = newDelta["movement"]

        i=0
        for t in self.tapes:
            t[i]= write[i]
            i+=1

        i=0
        for m in movements:
            if m == 'R':
                self.pos[i]+=1
            elif m == 'L':
                self.pos[i]-=1
            i+=1
        
        
        self.currentState = newDelta["newState"]

    # uq sig v
    # u= the left side of the head
    # q = current state
    # sig = the symbol in the head of the tape (tape[pos])
    # v= the right side of the head
    def __config__(self):
        u = self.tape[:self.pos]
        q = self.currentState
        sig = self.tape[self.pos]
        v = self.tape[self.pos+1:]

        config = "u: {u} , q: {q} , sig: {sig} v: {v}  ".format(u=u ,q=q ,sig=sig ,v=v)
        print(config)

    
    def runMachine(self):
        while self.currentState != "acc":
            symbols = []
            symbols = [self.tapes[i][self.pos[i]] for i in range(self.numOfTapes)]
            self.move(self.currentState, symbols)



    
class mulPQ(Tm):
    def __init__(self, tapes, currentState):
        
        states = {"start", "q1", "back", "acc"}
        
        deltaTable = {
            # start
            ("start", 1, 1, "_") : {"newState": "q1", "write": ['x', 1, '_'], "movement": ['R', 'S', 'S']},
            ("start", "_", 1, "_"): {"newState": "acc", "write": ['_', 1, '_'], "movement": ['S', 'S', 'S']},
            
            # q1
            ("q1", "_", "_", "_"): {"newState": "back", "write": ['_', "_", '_'], "movement": ['S', 'L', 'S']},
            ("q1", "1", "_", "_"): {"newState": "back", "write": ['1', "_", '_'], "movement": ['S', 'L', 'S']},

            ("q1", "_", 1, "_"): {"newState": "q1", "write": ['_', 1, 1], "movement": ['S', 'R', 'R']},
            ("q1", 1, 1, "_"): {"newState": "q1", "write": [1, 1, 1], "movement": ['S', 'R', 'R']},

            # back
            ("back", "_", 1, "_"): {"newState": "back", "write": ['_', 1, "_"], "movement": ['S', 'L', 'S']},
            ("back", 1, 1, "_"): {"newState": "back", "write": [1, 1, "_"], "movement": ['S', 'L', 'S']},

            ("back", "_", "_", "_"): {"newState": "start", "write": ['_', "_", "_"], "movement": ['S', 'R', 'S']},
            ("back", 1, "_", "_"): {"newState": "start", "write": [1, "_", "_"], "movement": ['S', 'R', 'S']}

        }


        super().__init__(tapes, states, currentState, deltaTable, 3)



t1 = [1, 1, 1]
t2 = [1, 1, 1, 1, 1]
m = mulPQ([t1, t2, []], "start").runMachine()
print(m)
