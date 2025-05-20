from itertools import product
from turtle import st
from tm2 import Tm
from utils2 import getHeadIndex
from .complement import complement
from .addition import Addition
import copy


class Subtraction(Tm):
   

    def __init__(self, tapes):
        """
            a class for a machine that computes a-b and addresses all the cases:
                * a,b >0
                * a, b <0
                * a>0, b<0
                * a<0, b>0
            
                the heads of tapes are in the left side of the numbers

                the first 2 tapes are copied
        """
        
        t1, t2 = tapes[0].copy(), tapes[1].copy()
        tapes = [t1, t2] + tapes[2:]
        if len(tapes)== 3:  # Ensure there are 3 tapes
            tapes[2].clear()
        

        deltaTable ={
            ("s", 0, "_", "_") : {"newState": "copyA", "movement": ['S', "S", "S"]},
            ("s", "_", "_", "_") : {"newState": "acc", "movement": ['S', "S", "S"]},

            ("s", 1, "_", "_") : {"newState": "copyA", "movement": ['S', "S", "S"]},

            ("s", "_", 0, "_") : {"newState": "copyB", "movement": ['S', "L", "S"]},
            ("s", "_", 1, "_") : {"newState": "copyB", "movement": ['S', "L", "S"]},

             ("goLeft", "_", "_", 0) : {"newState": "addMinus", "movement": ['S', "S", "L"]},
            ("goLeft", "_", "_", 1) : {"newState": "addMinus", "movement": ['S', "S", "L"]},

           

            # CASE 1: a,b>0
            # s-> case1
            ("s", 0, 0, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("s", 0, 1, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("s", 1, 0, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("s", 1, 1, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},

            # case1 -> case1 : going to the last digit in each number
            ("case1", 0, 0, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("case1", 0, 1, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("case1", 1, 0, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},
            ("case1", 1, 1, "_") : {"newState": "case1", "movement": ['R', "R", "S"]},

            ("case1", 0, "_", "_") : {"newState": "case1", "movement": ['R', "S", "S"]},
            ("case1", 1, "_", "_") : {"newState": "case1", "movement": ['R', "S", "S"]},

            ("case1", "_", 0, "_") : {"newState": "case1", "movement": ['S', "R", "S"]},
            ("case1", "_", 1, "_") : {"newState": "case1", "movement": ['S', "R", "S"]},

            # case1 -> zeros
            ("case1", "_", "_", "_") : {"newState": "zeros", "movement": ['L', "L", "S"]},

            # zeros-> zeros
            ("zeros", 0, 0, "_") : {"newState": "zeros", "movement": ['L', "L", "S"]},
            ("zeros", 0, 1, "_") : {"newState": "zeros", "movement": ['L', "L", "S"]},
            ("zeros", 1, 0, "_") : {"newState": "zeros", "movement": ['L', "L", "S"]},
            ("zeros", 1, 1, "_") : {"newState": "zeros", "movement": ['L', "L", "S"]},

            # complete the shorter number with zeros to the length of the longer number
            ("zeros", 0, "_", "_") : {"newState": "zeros", "write": [0, 0, "_"] , "movement": ['L', "L", "S"]},
            ("zeros", 1, "_", "_") : {"newState": "zeros", "write": [1, 0, "_"] , "movement": ['L', "L", "S"]},

            ("zeros", "_", 0, "_") : {"newState": "zeros", "write": [0, 0, "_"] , "movement": ['L', "L", "S"]},
            ("zeros", "_", 1, "_") : {"newState": "zeros", "write": [0, 1, "_"] , "movement": ['L', "L", "S"]},

            # zeros -> comp1
            ("zeros", "_", "_", "_") : {"newState": "comp1" , "movement": ['R', "S", "S"]},

           



            # carry -> carry
            ("carry", 0, "_", 0) : {"newState": "carry", "movement": ['R', "S", "R"]},
            ("carry", 0, "_", 1) : {"newState": "carry", "movement": ['R', "S", "R"]},
            ("carry", 1, "_", 0) : {"newState": "carry", "movement": ['R', "S", "R"]},
            ("carry", 1, "_", 1) : {"newState": "carry", "movement": ['R', "S", "R"]},
           

            # carry->endC : if c is longer than a there is a carry and we need to erase it
             ("carry", "_", "_", 0) : {"newState": "endC", "movement": ['S', "S", "L"]},
             ("carry", "_", "_", 1) : {"newState": "endC", "movement": ['S', "S", "L"]},

            #  endC-> endC
            ("endC", "_", "_", 0) : {"newState": "endC", "movement": ['S', "S", "L"]},
            ("endC", "_", "_", 1) : {"newState": "endC", "movement": ['S', "S", "L"]},

            # endC -> erase
            ("endC","_", "_", "_") : {"newState": "erase", "movement": ['S', "S", "R"]},

            # erase -> acc
            ("erase","_", "_", 1) : {"newState": "acc", "write": ["_", "_", "_"], "movement": ['S', "S", "S"]},


            # carry -> compResult: in case there isn't a carry, we need to convert the result to its 2's complement
            ("carry","_", "_", "_") : {"newState": "compResult", "movement": ['S', "S", "S"]},

            # compResult -> changeSign
            ("compResult", "_", "_", 0) : {"newState": "changeSign", "movement": ['S', "S", "L"]},
            ("compResult", "_", "_", 1) : {"newState": "changeSign", "movement": ['S', "S", "L"]},

            # changeSign -> acc
            ("changeSign", "_", "_", "_") : {"newState": "acc", "write": ["_", "_", "-"] , "movement": ['S', "S", "S"]},


            # CASE 2: a<0, b>0
            # for example: -9 - 5 . send them to the addition machine without the '-' sign and add the minus when finished

            # s -> add2
            ("s", "-", 0, "_") : {"newState": "add2", "write": ["_", 0, "_"], "movement": ['S', "L", "S"]},
            ("s", "-", 1, "_") : {"newState": "add2", "write": ["_", 1, "_"], "movement": ['S', "L", "S"]},

            # add2-> addMinus
            ("add2", "_", "_", 0) : {"newState": "addMinus", "movement": ['S', "S", "L"]},
            ("add2", "_", "_", 1) : {"newState": "addMinus", "movement": ['S', "S", "L"]},

            # addMinus -> acc
            ("addMinus", "_", "_", "_") : {"newState": "acc", "write": ["_", "_", "-"], "movement": ['S', "S", "S"]},
            

            # CASE 3: a>0, b<0
            # for example: 9 - (-5). delete the minus and send them to the addition machine to make it 9+5
            
            # s -> add3
            ("s", 0 , "-", "_") : {"newState": "add3", "write": [0, "_", "_"], "movement": ['S', "S", "S"]},
            ("s", 1 , "-", "_") : {"newState": "add3", "write": [1, "_", "_"], "movement": ['S', "S", "S"]},
        


            # CASE 4: both negative
            # for example: -9 - (-5): erase both '-', swap the tapes and send to the subtraction machine to get 5-9
            
            # s-> minus
            ("s", "-" , "-", "_") : {"newState": "minus", "write": ["_", "_", "_"], "movement": ['S', "S", "S"]},
        }


        for combo in product([0, 1, "_"], repeat=3):  
             # add1 -> carry: make sure that before checking the carry, the b tape would be on the "_" on the left of the tape
            deltaTable[("add1", *combo)] = {
                "newState": "carry",
                "movement": ['S', 'L', 'S']
            }
       

        super().__init__(tapes, "s", deltaTable, 3)



    
    def runMachine(self):
        steps = []
        while self.currentState != self.acc:
            if self.currentState == "comp1":
                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(self.tapes[1])
                }
                sts = complement(self.tapes[1])  # converts b to its two's complement
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 1,
                    "tape": self.tapes[1].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "add1"

            elif self.currentState == "add1":
                addMachine = Addition(self.tapes)

                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(addMachine.tapes)
                }

                sts = addMachine.runMachine()  # c = a + b' (b' is the two's complement of b)
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.pos[2] = getHeadIndex(self.tapes[2])  # updates the position of tape c
                # at this point a and c tapes are both positioned at the beginning of the numbers.
                # in the carry's state we would want to compare their lengths
                self.pos[1] = getHeadIndex(self.tapes[1])

                step = self.step()  # would move the b tape to a "_" before the first character for the carry checking
                steps.append(step)

            elif self.currentState == "compResult":
                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(self.tapes[2])
                }

                sts = complement(self.tapes[2])
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.pos[2] = getHeadIndex(self.tapes[2])

                step = self.step()
                steps.append(step)

            elif self.currentState == "add2":
                addMachine = Addition(self.tapes)

                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(addMachine.tapes)
                }

                sts = addMachine.runMachine()  # c = a + b
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.pos[2] = getHeadIndex(self.tapes[2])
                step = self.step()
                steps.append(step)

            elif self.currentState == "add3":
                addMachine = Addition(self.tapes)

                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(addMachine.tapes)
                }

                sts = addMachine.runMachine()  # c = a + b
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "acc"

            elif self.currentState == "minus":
                subMachine = Subtraction([self.tapes[1], self.tapes[0], self.tapes[2]])

                subMachineStep = {
                    "action": "submachine",
                    "tapes": copy.deepcopy(subMachine.tapes)
                }

                sts = subMachine.runMachine()  # c = b - a
                subMachineStep["steps"] = sts
                steps.append(subMachineStep)

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "acc"

            elif self.currentState == "copyA":
                Tm.copyTape(self.tapes[0], self.tapes[2])  # copy a to the result when it's a-0

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.currentState = "acc"

            elif self.currentState == "copyB":
                Tm.copyTape(self.tapes[1], self.tapes[2])  # copy b to the result and add - in the end in case of 0-b

                updateTapeStep = {
                    "action": "updateTape",
                    "tape_index": 2,
                    "tape": self.tapes[2].copy()
                }
                steps.append(updateTapeStep)

                self.pos[2] = getHeadIndex(self.tapes[2])
                self.currentState = "goLeft"

            else:
                step = self.step()
                steps.append(step)

        return steps

