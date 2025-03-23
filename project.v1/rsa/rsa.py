from basicMachines.mulMachine import mulMachine
from tm import Tm
from utils import unaryToDecimal
from .Euclid import Euclid
from .phi import phiN
from .squere.square import SquereM

class Rsa():
    """
    a class that implements RSA with a turing machine
        - fields: a, b, p, q, n, phi(n)
        - methods: 
            - A constructor that gets: p, q, b
            - Keys creation method
            - Encryption method
            - Decryption method
    """

    def __init__(self, p: int , q:int , b: int):
        """
        each one of the parameters are integers
        """
        self.p =  ["1" for i in range(p)]
        self.q = ["1" for i in range(q)]
        self.b = ["1" for i in range(b)]
        self.n = []
        self.phi = []

    
    def keys(self):
        """
        a method that creates the keys of the RSA
            - public key (b, n): n is created with the multiplication machine
            - private key (p, q, a): a is created with the euclides machine
        """

        # public key
        mulMachine([self.p, self.q, self.n]).runMachine() #n = p*q

        # private key
        phiN([self.p, self.q, self.phi]) #phi = phi(n)
        euclidesM = Euclid([self.phi, self.b]) 
        euclidesM.runEuclidAbstract() #phi*s + b*t = d
        self.a = euclidesM.t()
        Tm.trim_ones(self.a)

    
    def encryption(self, x: int):
        """
        gets the numeric plain text and encrypts it using a turing machine
            - with the public key (b, n), computes y = x^b mod n
        """
        if len(self.n) == 0:
            raise ValueError("need to execute the 'keys() methods first")
        
        x = ["1" for i in range(x)]
        squareMachine = SquereM([x, self.b, self.n])
        squareMachine.runMachine()
        result = squareMachine.result()
        return f"y= {result} \ny in a number: {unaryToDecimal(result)}"
    


    def __repr__(self):
        return (f"Public key: (b= {unaryToDecimal(self.b)}, n= {unaryToDecimal(self.n)})\n"
                f"b: {self.b} \n"
                f"n: {self.n} \n\n"
                
                f"Private key: (a= {unaryToDecimal(self.a)}, p= {unaryToDecimal(self.p)} , q= {unaryToDecimal(self.q)})\n"
                f"a: {self.a} \n"
                f"p: {self.p}\n"
                f"q: {self.q} \n")



