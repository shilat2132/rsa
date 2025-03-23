from tm2 import Tm
from .subtraction import Subtraction
from utils2 import getHeadIndex, getLastCharIndex

class Division(Tm):
    """
    a machine to get the integer part of the division of a /b and the remainder with the long division method
    """

    def __init__(self, tapes):
        """
            tapes = [a, b, m, r, d]
            * tapes a and b are required, all the others are optional.
            * m = a%b, d = a//b

        """

        # clears m, r, d if they are given
        if len(tapes) >2:
            for t in range(2, len(tapes)):
                tapes[t].clear()
        deltaTable = {
            #start -> addMinus
            ("start", "-", 0, "_", "_", "_") : {"newState": "addMinus", "write": ["_", 0, "_", "_", "-"] , "movement": ['R', "S", "S", "S", "R"]},
            ("start", "-", 1, "_", "_", "_") : {"newState": "addMinus", "write": ["_", 1, "_", "_", "-"] , "movement": ['R', "S", "S", "S", "R"]},
           

            # start -> initM
            # need to start from the first 1 digit, not 0
            ("start", 0, 0, "_", "_", "_") : {"newState": "start" , "movement": ['R', "R", "S", "S", "S"]},
            ("start", 0, 1, "_", "_", "_") : {"newState": "start" , "movement": ['R', "S", "S", "S", "S"]},
            ("start", 1, 0, "_", "_", "_") : {"newState": "start" , "movement": ['S', "R", "S", "S", "S"]},

            # ("start", 0, 0, "_", "_", "_") : {"newState": "initM", "write": [0, 0, 0, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            # ("start", 0, 1, "_", "_", "_") : {"newState": "initM", "write": [0, 1, 0, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            # ("start", 1, 0, "_", "_", "_") : {"newState": "initM", "write": [1, 0, 1, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            ("start", 1, 1, "_", "_", "_") : {"newState": "initM", "write": [1, 1, 1, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},

            # initM -> initM
            ("initM", 0, 0, "_", "_", "_") : {"newState": "initM", "write": [0, 0, 0, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            ("initM", 0, 1, "_", "_", "_") : {"newState": "initM", "write": [0, 1, 0, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            ("initM", 1, 0, "_", "_", "_") : {"newState": "initM", "write": [1, 0, 1, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},
            ("initM", 1, 1, "_", "_", "_") : {"newState": "initM", "write": [1, 1, 1, "_", "_"] , "movement": ['R', "R", "R", "S", "S"]},


            # initM -> sub
            ("initM", 0, "_", "_", "_", "_") : {"newState": "sub" , "movement": ['S', "S", "S", "S", "S"]},
            ("initM", 1, "_", "_", "_", "_") : {"newState": "sub" , "movement": ['S', "S", "S", "S", "S"]},
            ("initM", "_", 0, "_", "_", "_") : {"newState": "endB" , "movement": ['S', "R", "S", "S", "S"]},
            ("initM", "_", 1, "_", "_", "_") : {"newState": "endB" , "movement": ['S', "R", "S", "S", "S"]},
            ("initM", "_", "_", "_", "_", "_") : {"newState": "sub" , "movement": ['S', "S", "S", "S", "S"]},

            # endB -> endB
            ("endB", "_", 0, "_", "_", "_") : {"newState": "endB" , "movement": ['S', "R", "S", "S", "S"]},
            ("endB", "_", 1, "_", "_", "_") : {"newState": "endB" , "movement": ['S', "R", "S", "S", "S"]},

            # endB -> sub
            ("endB", "_", "_", "_", "_", "_") : {"newState": "sub" , "movement": ['S', "S", "S", "S", "S"]},

            # sub -> check
            # if the subtraction is negative, write 0 in the d tape
            ("sub", 0, "_", "_", "-", "_") : {"newState": "check", "write": [ 0, "_", "_", "-", 0] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", 1, "_", "_", "-", "_") : {"newState": "check", "write": [ 1, "_", "_", "-", 0] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", "_", "_", "_", "-", "_") : {"newState": "check", "write": [ "_", "_", "_", "-", 0] , "movement": ['S', "S", "S", "S", "R"]},

            # sub -> copyR
            # if the subtraction is non-negative, write 1 in the d tape
            ("sub", 0, "_", "_", 0, "_") : {"newState": "copyR", "write": [ 0, "_", "_", 0, 1] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", 1, "_", "_", 0, "_") : {"newState": "copyR", "write": [ 1, "_", "_", 0, 1] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", "_", "_", "_", 0, "_") : {"newState": "copyR", "write": [ "_", "_", "_", 0, 1] , "movement": ['S', "S", "S", "S", "R"]},

            ("sub", 0, "_", "_", 1, "_") : {"newState": "copyR", "write": [ 0, "_", "_", 1, 1] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", 1, "_", "_", 1, "_") : {"newState": "copyR", "write": [ 1, "_", "_", 1, 1] , "movement": ['S', "S", "S", "S", "R"]},
            ("sub", "_", "_", "_", 1, "_") : {"newState": "copyR", "write": [ "_", "_", "_", 1, 1] , "movement": ['S', "S", "S", "S", "R"]},


            # copyR -> check
            ("copyR", 0, "_", 0, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", 1, "_", 0, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", "_", "_", 0, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},

            ("copyR", 0, "_", 0, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", 1, "_", 0, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", "_", "_", 0, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},

            ("copyR", 0, "_", 1, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", 1, "_", 1, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", "_", "_", 1, 0, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},

            ("copyR", 0, "_", 1, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", 1, "_", 1, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},
            ("copyR", "_", "_", 1, 1, "_") : {"newState": "check" , "movement": ['S', "S", "R", "S", "S"]},


            # check -> acc
            ("check", "_", "_", "_", "_", "_") : {"newState": "acc" , "movement": ['S', "S", "S", "S", "S"]},

            # check -> aDown
            ("check", 0, "_", "_", "_", "_") : {"newState": "aDown" , "movement": ['S', "S", "S", "S", "S"]},
            ("check", 1, "_", "_", "_", "_") : {"newState": "aDown" , "movement": ['S', "S", "S", "S", "S"]},

            # aDown -> sub
            # copies a digit from a to m
            ("aDown", 0, "_", "_", "_", "_") : {"newState": "sub", "write": [ 0, "_", 0, "_", "_"] , "movement": ['R', "S", "R", "S", "S"]},
            ("aDown", 1, "_", "_", "_", "_") : {"newState": "sub", "write": [ 1, "_", 1, "_", "_"] , "movement": ['R', "S", "R", "S", "S"]},

        }

        super().__init__(tapes, "start", deltaTable, 5)

  

    # [0: a, 1: b, 2: m, 3: r, 4: d]
    def runMachine(self):
       """
       * tapes[2] = a%b
       * tapes[4] = a//b
       """
       while self.currentState != self.acc:
            if self.currentState == "sub":
               Subtraction([self.tapes[2], self.tapes[1], self.tapes[3]]).runMachine() # r = m -b
               self.pos[3] = getHeadIndex(self.tapes[3]) #set the position of the r tape
               self.step()
            
            elif self.currentState == "check":
                Tm.emptyTape(self.tapes[3]) #clear the tape of r
                self.step()

            elif self.currentState == "copyR":
                Tm.copyTape(self.tapes[3], self.tapes[2]) #m = r
                self.pos[2] = getLastCharIndex(self.tapes[2]) #set the position of the m tape
                self.step()

            elif self.currentState == "addMinus":
                self.currentState = "start"
                self.runMachine()
                # m = b - a%b = b -m
                Subtraction([self.tapes[1], self.tapes[2],  self.tapes[2]]).runMachine()
                break

            else:
                self.step()


        
        # [0: a, 1: b, 2: m, 3: r, 4: d]
    def getRemainderTape(self):
        return self.tapes[2]
    
    def getQuotient(self):
        return self.tapes[4]

