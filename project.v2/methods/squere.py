from operations.multiplication import Multiplication
from operations.division import Division
from tm2 import Tm
from utils2 import binaryToDecimal
from itertools import product


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
            ("q0", 1, "_", 1, "_", 0) : {"newState": "acc",  "movement": ['S', 'S', 'S', 'S', 'S']},

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
        
        # self.tapes = [x, b, n, m, y]
        # print(f"b in binary: {''.join(map(str, self.tapes[1]))}")
        # expDecimal=0
        # nDecimal = binaryToDecimal(self.tapes[2])
        # xDecimal = binaryToDecimal(self.tapes[0])

        # final = f"{xDecimal} ^ {binaryToDecimal(self.tapes[1])} mod {nDecimal} = ("

        while self.currentState != "acc":
            if self.currentState == "remainder0":
                tapes = [self.tapes[0], self.tapes[2], self.tapes[4]] #tapes = [x, n, y]
                Division(tapes).runMachine()

                # result = binaryToDecimal(self.tapes[0])
                # final+= str(result) + "* "
                # print(f"x^{2**expDecimal} mod b = {result}")

                self.currentState = "initM"

            elif self.currentState == "copyM":
                Tm.copyTape(self.tapes[0], self.tapes[3]) # m = x
                self.currentState = "loop"

            elif self.currentState == "loop":
                # expDecimal+=1
                # raise m to the power of 2
                t = self.tapes[3]
                Multiplication([t, t, t]).runMachine() #m = m^2
                

                # compute the mod of m^2
                tapes = [self.tapes[3].copy(), self.tapes[2], self.tapes[3]] #tapes = [m, n, m]
                Division(tapes).runMachine() #m = m%n

                self.step() #activate the transition in the delta table
            
            elif self.currentState=="updateY":
                # result = binaryToDecimal(self.tapes[3])
                # final+= str(result) + "* "
                # print(f"x^{2**expDecimal} mod n = {result}")

                    # compute y = (y*m)%n
                # compute y=y*m
                tapes = [self.tapes[4], self.tapes[3], self.tapes[4]] #tapes = [y, m, y]
                Multiplication(tapes).runMachine() #y = y*m
               

                # compute y = y%n
                tapes = [self.tapes[4].copy(), self.tapes[2], self.tapes[4]] #tapes = [y, n, y]
                Division(tapes).runMachine() #y = y%n
               
                self.currentState = "checkCond"
            
            else:
                
                self.step()
        
        # print(f"{final[:-2]}) mod {nDecimal} = {binaryToDecimal(self.tapes[4])}")
                
                    
            
            


    def result(self):
        return self.tapes[4]



