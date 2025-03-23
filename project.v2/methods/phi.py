from operations.multiplication import Multiplication
from operations.subtraction import Subtraction



def phiN(tapes):
    """
    tapes: a list of 3 lists - the 2 first are p and q and the third one is the list in which the result would be stored
    - given prime numbers p and q in binary base, each one is a list - compute phi(n)
    - n = p*q
    - subtract 1 from each one and multiply them to get phi(n)
    
    """

  
   
    p1 = []
    Subtraction([tapes[0], [1], p1]).runMachine() #p1 = p-1

    q1 = []
    Subtraction([tapes[1], [1], q1]).runMachine() #q1 = q-1
   
    
    Multiplication([q1, p1, tapes[2]]).runMachine()



    

   



