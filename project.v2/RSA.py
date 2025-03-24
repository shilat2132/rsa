from methods.phi import phiN
from methods.squere import Squere
from operations.multiplication import Multiplication
from utils2 import binaryToDecimal
from methods.euclidis import Euclid
from utils2 import decimalToBinaryList



class RSA():

    def __init__(self, p: list, q: list, b: list):
        self.x = None
        self.b = b
        self.p = p
        self.q = q

        self.y = None
        self.n = []
        self.phi = []
        self.a = []

        self.keyGeneration()

    

    def keyGeneration(self):
        """
        private key: (p, q, a) - 
            * compute phi = (p-1)(q-1)
            * compute a with the euclides algorithm

        public key: (b, n) -
            * compute n with the multiplication machine
        """
        phiN([self.p, self.q, self.phi])
        Multiplication([self.p, self.q, self.n]).runMachine()
        euclidMachine = Euclid([self.phi, self.b])
        euclidMachine.runMachine()
        self.a = euclidMachine.t()


    def encrypt(self, x: int):
        xList = decimalToBinaryList(x)

        square = Squere([xList, self.b, self.n])
        square.runMachine()
        print(f"The encrypted value of {x} is: {binaryToDecimal(square.result())}")

    def __repr__(self):
        """
            string representation of the RSA fields
        """
        rsa = f""" 
        n = {binaryToDecimal(self.n)},
        phi = {binaryToDecimal(self.phi)},
        a = {binaryToDecimal(self.a)}
        """
       
        return rsa