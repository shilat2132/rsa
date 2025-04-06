from operations.division import Division
from operations.multiplication import Multiplication
from operations.subtraction import Subtraction
from tm2 import Tm
from utils2 import isZero


class Euclid(Tm):
    """
    [r(i-1), r(i), s(i-1), s(i), t(i-1), t(i), q, m]
    """
    def __init__(self, tapes):
        """
        initiates the Euclid tm fields
            - tapes: a list with a and b of the gcd -> gcd(a,b)
            
        """
        tapes[0] = tapes[0].copy()
        tapes[1] = tapes[1].copy()
        deltaTable = {
            # start set the values of s0, s1, t0, t1
            ("start", 0, 0, "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": [0, 0, 1, "_", "_", 1, "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]},
            ("start", 0, 1, "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": [0, 1, 1, "_", "_", 1, "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]},
            ("start", 1, 0, "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": [1, 0, 1, "_", "_", 1, "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]},
            ("start", 1, 1, "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": [1, 1, 1, "_", "_", 1, "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]},
        }






        super().__init__(tapes, "start", deltaTable, 8)
        self.tapesDict= {
            "r(i-1)": 0,
            "r(i)": 1,

            "s(i-1)": 2,
            "s(i)": 3,

            "t(i-1)": 4,
            "t(i)": 5,

            "q": 6,
            "m": 7,
        }

        # a and b are kept in case the result of t or s are negative an a negative remainder formola is needed
        self.ring1 = tapes[0].copy() #a
        self.ring2 = tapes[1].copy() #b

    def runMachine(self):
        while self.currentState != "acc":
            if self.currentState == "computeQ":
                # q = r(i-1)// ri
                d = Division([self.tapes[0], self.tapes[1]])
                d.runMachine()
                
                # copy quotient to q
                Tm.copyTape(d.getQuotient(), self.tapes[6])

                self.currentState = "r"

            
            if self.currentState == "r":
                # rip1 = rim1 - q* ri
                Euclid.Rst(self.tapes[0], self.tapes[1], self.tapes[6], self.tapes[7])
                self.currentState = "s"
            
            if self.currentState == "s":
                # sip1 = sim1 - q* si
                Euclid.Rst(self.tapes[2], self.tapes[3], self.tapes[6], self.tapes[7])
                self.currentState = "t"

            if self.currentState == "t":
                # tip1 = tim1 - q* ti
                Euclid.Rst(self.tapes[4], self.tapes[5], self.tapes[6], self.tapes[7])

                self.currentState = "checkCond"

            if self.currentState == "checkCond":
                Tm.emptyTape(self.tapes[6])
                
                if isZero(self.tapes[1]) == True:
                    self.currentState = "acc"
                else:
                    self.currentState = "computeQ"
            
            else:
                self.step()


        # keep s and t in their proper ring: s*a + t*b -> s should be in ring b (ring 2) and t should be in ring a (ring 1)
        sIndex = self.tapesDict["s(i-1)"]
        tIndex = self.tapesDict["t(i-1)"]

        divMachine = Division([self.tapes[sIndex], self.ring2]) #s % b
        divMachine.runMachine()
        self.tapes[sIndex] = divMachine.getRemainder()


        divMachine = Division([self.tapes[tIndex], self.ring1]) #t % a
        divMachine.runMachine()
        self.tapes[tIndex] = divMachine.getRemainder()



    def Rst(vim1: list, vi: list, q: list, m: list):
        """
        computes: v(i+1) = v(i-1)+qi*vi, while the v is r, s or t of the euclides algorithm
        returns: the configuration string
        """
        Multiplication([vi, q, m]).runMachine() # m = q*vi
        Subtraction([vim1, m, m]).runMachine() # m = vim1 - m = vim1 - q*vi

        # vim1, vi = vi, vi+1
        Tm.copyTape(vi, vim1)
        Tm.copyTape(m, vi)

        Tm.emptyTape(m)

    def d(self):
        return self.tapes[0]
    def t(self):
        return self.tapes[self.tapesDict["t(i-1)"]]
    def s(self):
        return self.tapes[self.tapesDict["s(i-1)"]]

