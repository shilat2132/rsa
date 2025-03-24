from tm2 import Tm
from operations.multiplication import Multiplication
from operations.addition import Addition
from operations.division import Division

from .euclidis import Euclid


class Crt(Tm):

    def __init__(self, tapes):
        """
        this is a machine that computes crt with only 2 equations
        tapes should include: x1, x2, p, q
        """

        super().__init__(tapes, "start", {}, 9)

    
    def runMachine(self):
        tapesDict = {
            "x1": self.tapes[0],
            "x2": self.tapes[1],
            "M2": self.tapes[2], # = m1 = M/m2 = (m1*m2)/m2
            "M1": self.tapes[3], # = m2 = M/m1 = (m1*m2)/m1
            "y1": self.tapes[4],
            "y2": self.tapes[5],
            "M": self.tapes[6],
            "v": self.tapes[7], #extra tape for storing temperory results
            "result": self.tapes[8]
        }

        # compute M = m1*m2 = M1*M2
        Multiplication([tapesDict["M1"], tapesDict["M2"], tapesDict["M"]]).runMachine()

        # compute y1, y2 with euclides of (M1, M2)
        # s*M1 + t*M2 = d -> s=y1, t=y2
        euclidesMachine = Euclid([tapesDict["M1"], tapesDict["M2"]])
        euclidesMachine.runMachine()

        self.tapes[4] = euclidesMachine.s()
        tapesDict["y1"] = self.tapes[4]

        self.tapes[5] = euclidesMachine.t()
        tapesDict["y2"] = self.tapes[5]



        

        # COMPUTE THE SUM:( x1*M1*y1 + x2*M2*y2) mod M

        # v = x1*M1*y1
            # step 1: v = x1*M1
            # step 2: v = v* y1

        Multiplication([tapesDict["x1"], tapesDict["M1"], tapesDict["v"]]).runMachine()
        Multiplication([tapesDict["y1"], tapesDict["v"], tapesDict["v"]]).runMachine()

        # result = x2*M2*y2
            # step 1: result = x2*M2
            # step 2: result = result*y2

        Multiplication([tapesDict["x2"], tapesDict["M2"], tapesDict["result"]]).runMachine()
        Multiplication([tapesDict["y2"], tapesDict["result"], tapesDict["result"]]).runMachine()


        # result = result + v
        Addition([tapesDict["result"], tapesDict["v"], tapesDict["result"]]).runMachine()

        # result = result % M
        remainder = Division([tapesDict["result"], tapesDict["M"]])
        remainder.runMachine()

        self.tapes[8] = remainder.getRemainder()

    

    def getX(self):
        return  self.tapes[8]