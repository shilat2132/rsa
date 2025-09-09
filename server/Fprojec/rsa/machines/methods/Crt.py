from tm2 import Tm
from operations.multiplication import Multiplication
from operations.addition import Addition
from operations.division import Division
from utils2 import binaryToDecimal
from .euclidis import Euclid
import copy


class Crt(Tm):

    def __init__(self, tapes):
        """
        this is a machine that computes crt with only 2 equations
        tapes should include: x1, x2, p, q
        """

        super().__init__(tapes, "start", {}, 9)

    
    def runMachine(self):
        """
        returns the main step object of the CRT machine.
        """
        steps = []
        main_step = {
            "action": "main",
            "formula": "CRT: x = (x1 * M1 * y1 + x2 * M2 * y2) % M",
            "tapes": copy.deepcopy(self.tapes)
        }

        tapesDict = {
            "x1": self.tapes[0],
            "x2": self.tapes[1],
            "M2": self.tapes[2],  # = m1 = M/m2 = (m1*m2)/m2
            "M1": self.tapes[3],  # = m2 = M/m1 = (m1*m2)/m1
            "y1": self.tapes[4],
            "y2": self.tapes[5],
            "M": self.tapes[6],
            "v": self.tapes[7],  # extra tape for storing temporary results
            "result": self.tapes[8]
        }

        # compute M = m1*m2 = M1*M2
        mulMachine = Multiplication([tapesDict["M1"], tapesDict["M2"], tapesDict["M"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "M = m1 * m2",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # compute y1, y2 with euclides of (M1, M2)
        # s*M1 + t*M2 = d -> s=y1, t=y2
        euclidesMachine = Euclid([tapesDict["M1"], tapesDict["M2"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "Euclides: s * M1 + t * M2 = d -> s = y1, t = y2",
            "tapes": copy.deepcopy(euclidesMachine.tapes)
        }
        euclidSteps = euclidesMachine.runMachine()
        subMachineStep["steps"] = euclidSteps
        steps.append(subMachineStep)

        self.tapes[4] = euclidesMachine.s()
        tapesDict["y1"] = self.tapes[4]

        self.tapes[5] = euclidesMachine.t()
        tapesDict["y2"] = self.tapes[5]

        # COMPUTE THE SUM:( x1*M1*y1 + x2*M2*y2) mod M

        # v = x1*M1*y1
        # step 1: v = x1*M1
        mulMachine = Multiplication([tapesDict["x1"], tapesDict["M1"], tapesDict["v"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "v = x1 * M1",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # step 2: v = v * y1
        mulMachine = Multiplication([tapesDict["y1"], tapesDict["v"], tapesDict["v"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "v = v * y1 = x1 * M1 * y1",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # result = x2*M2*y2
        # step 1: result = x2*M2
        mulMachine = Multiplication([tapesDict["x2"], tapesDict["M2"], tapesDict["result"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "result = x2 * M2",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # step 2: result = result * y2
        mulMachine = Multiplication([tapesDict["y2"], tapesDict["result"], tapesDict["result"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "result = result * y2 = x2 * M2 * y2",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # result = result + v
        addMachine = Addition([tapesDict["result"], tapesDict["v"], tapesDict["result"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "result = result + v = x1 * M1 * y1 + x2 * M2 * y2",
            "tapes": copy.deepcopy(addMachine.tapes)
        }
        addSteps = addMachine.runMachine()
        subMachineStep["steps"] = addSteps
        steps.append(subMachineStep)

        # result = result % M
        divMachine = Division([tapesDict["result"], tapesDict["M"]])
        subMachineStep = {
            "action": "submachine",
            "formula": "result = result % M = (x1 * M1 * y1 + x2 * M2 * y2) % M",
            "tapes": copy.deepcopy(divMachine.tapes)
        }
        divSteps = divMachine.runMachine()
        subMachineStep["steps"] = divSteps
        steps.append(subMachineStep)

        self.tapes[8] = divMachine.getRemainder()
        tapesDict["result"] = self.tapes[8]

        main_step["steps"] = steps

        return main_step
    

    def getX(self):
        return  self.tapes[8]



