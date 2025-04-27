from turtle import st
from operations.multiplication import Multiplication
from operations.division import Division
from tm2 import Tm
from utils2 import binaryToDecimal
from itertools import product
import copy


class Squere(Tm):
    """
        a class for Exponentiation by Squaring.
        - has 5 tapes
        - gets the input in the tapes of: [x, b, n] 
        - computes (x^b) % n and stores the result in y, i.e the fifth tape
        - tapes = [x, b, n, m, y]
    """

    def __init__(self, tapes):

        deltaTable ={
            # q0 -> q0
            # runs until the last digit of b
            ("q0", 0, 0, 0, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},
            ("q0", 0, 1, 0, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},

            ("q0", 0, 0, 1, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},
            ("q0", 0, 1, 1, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},

            ("q0", 1, 0, 0, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},
            ("q0", 1, 1, 0, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},

            ("q0", 1, 0, 1, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},
            ("q0", 1, 1, 1, "_", "_") : {"newState": "q0",  "movement": ['S', 'R', 'S', 'S', 'S']},


            # q0 -> initY
            ("q0", 0, "_", 0, "_", "_") : {"newState": "initY",  "movement": ['S', 'L', 'S', 'S', 'S']},
            ("q0", 0, "_", 1, "_", "_") : {"newState": "initY",  "movement": ['S', 'L', 'S', 'S', 'S']},
            ("q0", 1, "_", 0, "_", "_") : {"newState": "initY",  "movement": ['S', 'L', 'S', 'S', 'S']},
            ("q0", 1, "_", 1, "_", "_") : {"newState": "initY",  "movement": ['S', 'L', 'S', 'S', 'S']},
            

            # initY -> remainder0 
            # if binary[k]==1:  y = x%n
            
            ("initY", 0, 1, 0, "_", "_") : {"newState": "remainder0", "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 0, 1, 1, "_", "_") : {"newState": "remainder0", "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 1, 1, 0, "_", "_") : {"newState": "remainder0",  "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 1, 1, 1, "_", "_") : {"newState": "remainder0", "movement": ['S', 'L', 'S', 'S', 'S']}, 

            # initY -> initM
            # if binary[k]== 0: y=1
            ("initY", 0, 0, 0, "_", "_") : {"newState": "initM", "write": [0, 0, 0 , '_', 1], "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 0, 0, 1, "_", "_") : {"newState": "initM", "write": [0, 0, 1 , '_', 1], "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 1, 0, 0, "_", "_") : {"newState": "initM", "write": [1, 0, 0 , '_', 1], "movement": ['S', 'L', 'S', 'S', 'S']}, 
            ("initY", 1, 0, 1, "_", "_") : {"newState": "initM", "write": [1, 0, 1 , '_', 1], "movement": ['S', 'L', 'S', 'S', 'S']}, 
             

            # initM -> acc  

            ("q0", 0, "_", 0, "_", 0) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 0, "_", 1, "_", 0) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 1, "_", 0, "_", 0) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 1, "_", 1, "_", 0) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S'],},

            ("q0", 0, "_", 0, "_", 1) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 0, "_", 1, "_", 1) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 1, "_", 0, "_", 1) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("q0", 1, "_", 1, "_", 1) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},

            # initM -> copyM
            #  if k>=0: m = x 
            ("initM", "1", "0", "1", "_", "1") : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", "1", "1", "1", "_", "1") : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},

            ("initM", 0, 0, 0, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 0, 0, 1, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 0, 0, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 0, 1, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},

            ("initM", 0, 0, 0, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 0, 0, 1, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 0, 0, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 0, 1, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},

             ("initM", 0, 1, 0, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 0, 1, 1, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 1, 0, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 1, 1, "_", 0) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},

            ("initM", 0, 1, 0, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 0, 1, 1, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 1, 0, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("initM", 1, 1, 1, "_", 1) : {"newState": "copyM",  "movement": ['S', 'S', 'S', 'S', 'S']},


            # loop -> checkCond - done
            ("loop", "1", "0", "1", "1", "1") : {"newState": "checkCond",  "movement": ['S', 'L', 'S', 'S', 'S']}, 

            # loop -> updateY - done
            ("loop", "1", "1", "1", "1", "1") : {"newState": "updateY",  "movement": ['S', 'L', 'S', 'S', 'S']},

            # checkCond -> loop
            ("checkCond", "1", "0", "1", "1", "1") : {"newState": "loop",  "movement": ['S', 'S', 'S', 'S', 'S']},
            ("checkCond", "1", "1", "1", "1", "1") : {"newState": "loop",  "movement": ['S', 'S', 'S', 'S', 'S']},

            #checkCond -> acc
            ("checkCond", "1", "_", "1", "1", "1") : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},


        }

        # product creates all the possible combination of 0 and 1 in length of 5 in order to 
        # dynamically create transitions with lots of combinations 
        for combo in product([0, 1], repeat=5):  # 
            
            # loop -> checkCond / updateY
            deltaTable[("loop", *combo)] = {
                # if binary[k] == 0: skip to checkCond
                "newState": "checkCond" if combo[1] == 0 else "updateY",
                "movement": ['S', 'L', 'S', 'S', 'S']
            }

            # checkCond -> loop
            deltaTable[("checkCond", *combo)] = {
                #  while k>=0:
                "newState": "loop",
                "movement": ['S', 'S', 'S', 'S', 'S']
            }

        
        for combo in product([0, 1], repeat=4):
             # checkCond -> acc
            c1 = (combo[0], "_") + combo[1:]
            deltaTable[("checkCond", *c1)] = {
                #  end loop - k< 0:
                "newState": "acc",
                "movement": ['S', 'S', 'S', 'S', 'S']
            }

        super().__init__(tapes, "q0", deltaTable, 5)


    
    def runMachine(self):
        """
        Runs the exponentiation by squaring machine.
        returns the steps list.
        """
        steps = []

        while self.currentState != "acc":
            if self.currentState == "remainder0":
                # compute y = x % n
                divMachine = Division([self.tapes[0], self.tapes[2], self.tapes[4]])  # Division machine for y = x % n
                subMachineStep = {
                    "action": "submachine",
                    "formula": "y = x % n",
                    "tapes": copy.deepcopy(divMachine.tapes)
                }
                divisionSteps = divMachine.runMachine()
                subMachineStep["steps"] = divisionSteps
                steps.append(subMachineStep)

                self.currentState = "initM"

            elif self.currentState == "copyM":
                # m = x
                Tm.copyTape(self.tapes[0], self.tapes[3])
                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 3,
                    "tape": self.tapes[3].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "loop"

            elif self.currentState == "loop":
                # raise m to the power of 2
                t = self.tapes[3]
                mulMachine = Multiplication([t, t, t])  # Multiplication machine for m = m^2
                subMachineStep = {
                    "action": "submachine",
                    "formula": "m = m^2",
                    "tapes": copy.deepcopy(mulMachine.tapes)
                }
                multiplicationSteps = mulMachine.runMachine()
                subMachineStep["steps"] = multiplicationSteps
                steps.append(subMachineStep)

                # compute the mod of m^2
                divMachine = Division([self.tapes[3], self.tapes[2], self.tapes[3]])  # Division machine for m = m % n
                subMachineStep = {
                    "action": "submachine",
                    "formula": "m = m % n",
                    "tapes": copy.deepcopy(divMachine.tapes)
                }
                divisionSteps = divMachine.runMachine()
                subMachineStep["steps"] = divisionSteps
                steps.append(subMachineStep)

                # Log the step transition
                step = self.step()  # Activate the transition in the delta table
                steps.append(step)

            elif self.currentState == "updateY":
                # compute y = (y * m) % n
                # compute y = y * m
                mulMachine = Multiplication([self.tapes[4], self.tapes[3], self.tapes[4]])  # Multiplication machine for y = y * m
                subMachineStep = {
                    "action": "submachine",
                    "formula": "y = y * m",
                    "tapes": copy.deepcopy(mulMachine.tapes)
                }
                multiplicationSteps = mulMachine.runMachine()
                subMachineStep["steps"] = multiplicationSteps
                steps.append(subMachineStep)

                # compute y = y % n
                divMachine = Division([self.tapes[4], self.tapes[2], self.tapes[4]])  # Division machine for y = y % n
                subMachineStep = {
                    "action": "submachine",
                    "formula": "y = y % n",
                    "tapes": copy.deepcopy(divMachine.tapes)
                }
                divisionSteps = divMachine.runMachine()
                subMachineStep["steps"] = divisionSteps
                steps.append(subMachineStep)

                self.currentState = "checkCond"

            else:
                # Log the step transition
                step = self.step()  # Activate the transition in the delta table
                steps.append(step)

        return steps
    def result(self):
        return self.tapes[4]



