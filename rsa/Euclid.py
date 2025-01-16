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
        self.ring1 = tapes[0] #a
        self.ring2 = tapes[1] #b

    
    def runEuclidAbstract(self):
        self.step() #assigns the initializes values of the euclid algorithm
        
        while self.currentState != "acc":
            # currentState= computeQ
            qMachine = divMachine([self.tapes[self.tapesDict["r(i-1)"]], self.tapes[self.tapesDict["r(i)"]]]) #q = r(i-1) // r(i)
            qMachine.runMachine()
            Tm.copyTape(qMachine.resultTape(), self.tapes[self.tapesDict["q"]])

            self.currentState = "r"
            Euclid.Rst(self.tapes[self.tapesDict["r(i-1)"]],
                     self.tapes[self.tapesDict["r(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "s"
            Euclid.Rst(self.tapes[self.tapesDict["s(i-1)"]],
                     self.tapes[self.tapesDict["s(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "t"
            Euclid.Rst(self.tapes[self.tapesDict["t(i-1)"]],
                     self.tapes[self.tapesDict["t(i)"]], 
                     self.tapes[self.tapesDict["q"]], 
                     self.tapes[self.tapesDict["m"]])
            
            self.currentState = "emptyQ"
            Tm.emptyTape(self.tapes[self.tapesDict["q"]])

            rHead = getHeadIndex(self.tapes[1])
            if self.tapes[1][rHead] == "_":
                self.currentState = "acc"
            else: self.currentState = "computeQ"

        # compute t and s in the Z ring of the original number given in the second tape(for example Z 26)
            # it would be done using the remainder machine
            # sa+tb=d
        aTapeS = self.tapes[self.tapesDict['s(i-1)']]
        bTapeS = self.ring2
        remainderMachineS = remainderMachine([aTapeS, bTapeS]) #s%b
        remainderMachineS.runMachine()
        Tm.copyTape(remainderMachineS.tapes[2], self.tapes[self.tapesDict['s(i-1)']]) #s = s%b


        aTapeT = self.tapes[self.tapesDict['t(i-1)']]
        bTapeT = self.ring1
        remainderMachineT = remainderMachine([aTapeT, bTapeT]) #t%a
        remainderMachineT.runMachine()
        Tm.copyTape(remainderMachineT.tapes[2], self.tapes[self.tapesDict['t(i-1)']]) #t = t%a

    
    def Rst(vim1: list, vi: list, q: list, m: list):
        qvMachine = mulMachine([q, vi])
        qvMachine.runMachine() 
        Tm.copyTape(qvMachine.result(), m) #m = q*vi

        # v(i-1) = v(i-1) - q*v(i)
        subMachine(vim1, m)

        
        Tm.copyTape(vim1, m) # m = v(i-1)
        Tm.copyTape(vi, vim1) #v(i-1) = v(i)
        Tm.copyTape(m, vi) # v(i) = m = v(i-1) - q*v(i)
        Tm.emptyTape(m)

    def d(self):
        return self.tapes[self.tapesDict["r(i-1)"]]
    def t(self):
        return self.tapes[self.tapesDict["t(i-1)"]]
    def s(self):
        return self.tapes[self.tapesDict["s(i-1)"]]

