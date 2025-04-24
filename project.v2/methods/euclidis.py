from operations.division import Division
from operations.multiplication import Multiplication
from operations.subtraction import Subtraction
from tm2 import Tm
from utils2 import isZero
import copy


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
        """ returns the steps list of the machine """
        steps = []
        while self.currentState != "acc":
            if self.currentState == "computeQ":
                # q = r(i-1) // r(i)
                d = Division([self.tapes[0], self.tapes[1]])
                subMachineStep = {
                    "action": "submachine",
                    "formula": "q = r(i-1) // r(i)",
                    "tapes": copy.deepcopy(d.tapes)
                }
                sts = d.runMachine()
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                # copy quotient to q
                Tm.copyTape(d.getQuotient(), self.tapes[6])
                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 6,
                    "tape": self.tapes[6].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "r"

            if self.currentState == "r":
                # r(i+1) = r(i-1) - q * r(i)
                tapes = [self.tapes[0], self.tapes[1], self.tapes[6], self.tapes[7]]
                subMachineStep = {
                    "action": "submachine",
                    "formula": "r(i+1) = r(i-1) - q * r(i)",
                    "tapes": copy.deepcopy(tapes)
                }
                rstSteps = Euclid.Rst(*tapes)
                subMachineStep["steps"] = rstSteps
                steps.append(subMachineStep)

               

                self.currentState = "s"

            if self.currentState == "s":
                # s(i+1) = s(i-1) - q * s(i)
                tapes = [self.tapes[2], self.tapes[3], self.tapes[6], self.tapes[7]]
                subMachineStep = {
                    "action": "submachine",
                    "formula": "s(i+1) = s(i-1) - q * s(i)",
                    "tapes": copy.deepcopy(tapes)
                }
                rstSteps = Euclid.Rst(*tapes)
                subMachineStep["steps"] = rstSteps
                steps.append(subMachineStep)

               

                self.currentState = "t"

            if self.currentState == "t":
                # t(i+1) = t(i-1) - q * t(i)
                tapes = [self.tapes[4], self.tapes[5], self.tapes[6], self.tapes[7]]
                subMachineStep = {
                    "action": "submachine",
                    "formula": "t(i+1) = t(i-1) - q * t(i)",
                    "tapes": copy.deepcopy(tapes)
                }
                rstSteps = Euclid.Rst(*tapes)
                subMachineStep["steps"] = rstSteps
                steps.append(subMachineStep)

                self.currentState = "checkCond"

            if self.currentState == "checkCond":
                Tm.emptyTape(self.tapes[6])

                # it's always after the change of t so update machine step is here instead of in the 2 of them
                updateMachineStep = {
                    "action": "updateMachine",
                    "tapes": copy.deepcopy(self.tapes)
                }
                steps.append(updateMachineStep)

                if isZero(self.tapes[1]):
                    self.currentState = "acc"
                else:
                    self.currentState = "computeQ"

            else:
                step = self.step()
                steps.append(step)

        # keep s and t in their proper ring: s*a + t*b -> s should be in ring b (ring 2) and t should be in ring a (ring 1)
        sIndex = self.tapesDict["s(i-1)"]
        tIndex = self.tapesDict["t(i-1)"]

        divMachine = Division([self.tapes[sIndex], self.ring2])  # s % b
        subMachineStep = {
            "action": "submachine",
            "tapes": copy.deepcopy(divMachine.tapes)
        }
        sts = divMachine.runMachine()
        subMachineStep["steps"] = sts
        steps.append(subMachineStep)

        self.tapes[sIndex] = divMachine.getRemainder()
        updateTapeStep = {
            "action": "updateTape",
            "tape_index": sIndex,
            "tape": self.tapes[sIndex].copy()
        }
        steps.append(updateTapeStep)

        divMachine = Division([self.tapes[tIndex], self.ring1])  # t % a
        subMachineStep = {
            "action": "submachine",
            "tapes": copy.deepcopy(divMachine.tapes)
        }
        sts = divMachine.runMachine()
        subMachineStep["steps"] = sts
        steps.append(subMachineStep)

        self.tapes[tIndex] = divMachine.getRemainder()
        updateTapeStep = {
            "action": "updateTape",
            "tape_index": tIndex,
            "tape": self.tapes[tIndex].copy()
        }
        steps.append(updateTapeStep)

        return steps

    def Rst(vim1: list, vi: list, q: list, m: list):
        """
        computes: v(i+1) = v(i-1)+qi*vi, while the v is r, s or t of the euclides algorithm
        returns: the steps list
        """
        steps = []

        # Multiplication: m = q * vi
        tapes = [vi, q, m]
        mulMachine = Multiplication(tapes)
        subMachineStep = {
            "action": "submachine",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        sts = mulMachine.runMachine()
        subMachineStep["steps"] = sts
        steps.append(subMachineStep)

        # Subtraction: m = vim1 - m = vim1 - q * vi
        tapes = [vim1, m, m]
        subMachine = Subtraction(tapes)
        subMachineStep = {
            "action": "submachine",
            "tapes": copy.deepcopy(subMachine.tapes)
        }
        sts = subMachine.runMachine()
        subMachineStep["steps"] = sts
        steps.append(subMachineStep)

        # Copy vim1 <- vi
        Tm.copyTape(vi, vim1)

        # Copy vi <- m
        Tm.copyTape(m, vi)

        # Empty m
        Tm.emptyTape(m)

        return steps

    def d(self):
        return self.tapes[0]
    def t(self):
        return self.tapes[self.tapesDict["t(i-1)"]]
    def s(self):
        return self.tapes[self.tapesDict["s(i-1)"]]

