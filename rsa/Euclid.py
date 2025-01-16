from basicMachines.divMachine import divMachine
from basicMachines.mulMachine import mulMachine
from basicMachines.subMachine import subMachine
from basicMachines.remainderMachine import remainderMachine
from tm import Tm
from utils import getHeadIndex


class Euclid(Tm):
    """
    [r(i-1), r(i), s(i-1), s(i), t(i-1), t(i), q, m]
    """
    def __init__(self, tapes):
        """
        initiates the Euclid tm fields
            - tapes: a list with a and b of the gcd -> gcd(a,b)
            
        """
        states = {"start", "computeQ", "r", "s", "t", "emptyQ"}
        deltaTable = {
            ("start", "1", "1", "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": ["1", "1", "1", "_", "_", "1", "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]},
            ("start", "-", "1", "_", "_", "_", "_", "_", "_"): {"newState": "computeQ", "write": ["-", "1", "1", "_", "_", "1", "_", "_"], "movement": ["S", "S", "S", "S", "S", "S", "S", "S"]}
        }
        super().__init__(tapes, states, "start", deltaTable, 8)
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
        self.ring1 = tapes[0].copy() #a
        self.ring2 = tapes[1].copy() #b

    
    def runEuclidAbstract(self):
        """
        runs the euclidis machine abstracttly
        """
        config = Tm.config(self.tapes, self.currentState, self.pos) + "\n"
        self.step() #assigns the initializes values of the euclid algorithm
        config+= Tm.config(self.tapes, self.currentState, self.pos) + "\n"

        while self.currentState != "acc":
            # currentState= computeQ
            qMachine = divMachine([self.tapes[self.tapesDict["r(i-1)"]], self.tapes[self.tapesDict["r(i)"]]]) #q = r(i-1) // r(i)
            config+=qMachine.runMachine()
            config+=Tm.copyTape(qMachine.resultTape(), self.tapes[self.tapesDict["q"]])

            self.currentState = "r"
            config+=Euclid.Rst(self.tapes[self.tapesDict["r(i-1)"]],
                     self.tapes[self.tapesDict["r(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "s"
            config+=Euclid.Rst(self.tapes[self.tapesDict["s(i-1)"]],
                     self.tapes[self.tapesDict["s(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "t"
            config+= Euclid.Rst(self.tapes[self.tapesDict["t(i-1)"]],
                     self.tapes[self.tapesDict["t(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "emptyQ"
            config+=Tm.emptyTape(self.tapes[self.tapesDict["q"]])

            rHead = getHeadIndex(self.tapes[1])
            if self.tapes[1][rHead] == "_":
                self.currentState = "acc"
            else: self.currentState = "computeQ"

        # compute t and s in the Z ring of the original number given in the second tape(for example Z 26)
            # it would be done using the remainder machine
            # sa+tb=d
        tape1S = self.tapes[self.tapesDict['s(i-1)']]
        tape2S = self.ring2
        remainderMachineS = remainderMachine([tape1S, tape2S]) #s%b
        config+=remainderMachineS.runMachine()
        config+=Tm.copyTape(remainderMachineS.tapes[2], self.tapes[self.tapesDict['s(i-1)']]) #s = s%b


        tape1T = self.tapes[self.tapesDict['t(i-1)']]
        tape2T = self.ring1
        remainderMachineT = remainderMachine([tape1T, tape2T]) #t%a
        config+=remainderMachineT.runMachine()
        config+=Tm.copyTape(remainderMachineT.tapes[2], self.tapes[self.tapesDict['t(i-1)']]) #t = t%a

    
    def Rst(vim1: list, vi: list, q: list, m: list):
        """
        computes: v(i+1) = v(i-1)+qi*vi, while the v is r, s or t of the euclides algorithm
        returns: the configuration string
        """
        qvMachine = mulMachine([q, vi])
        config = qvMachine.runMachine() 
        config+=Tm.copyTape(qvMachine.result(), m) #m = q*vi

        # v(i-1) = v(i-1) - q*v(i)
        config+= subMachine(vim1, m)

        
        config+=Tm.copyTape(vim1, m) # m = v(i-1)
        config+=Tm.copyTape(vi, vim1) #v(i-1) = v(i)
        config+=Tm.copyTape(m, vi) # v(i) = m = v(i-1) - q*v(i)
        config+=Tm.emptyTape(m)

        return config

    def d(self):
        return self.tapes[self.tapesDict["r(i-1)"]]
    def t(self):
        return self.tapes[self.tapesDict["t(i-1)"]]
    def s(self):
        return self.tapes[self.tapesDict["s(i-1)"]]

