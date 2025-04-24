from calendar import c
from methods.phi import phiN
from methods.euclidis import Euclid
from methods.Crt import Crt
from methods.squere import Squere


from operations.multiplication import Multiplication
from operations.division import Division
from operations.subtraction import Subtraction

from utils2 import binaryToDecimal
from utils2 import decimalToBinaryList
import copy


class RSA():

    def __init__(self, p: list, q: list, b: list):
        """
        Holds the public and private keys of the RSA algorithm.
        """
        self.x = None
        self.b = b
        self.p = p
        self.q = q

        self.y = None
        self.n = []
        self.phi = []
        self.a = []

        # Store the key generation steps temporarily
        self._key_generation_steps = self.keyGeneration()

    def keyGeneration(self):
        """
        private key: (p, q, a) - 
            * compute phi = (p-1)(q-1)
            * compute a with the Euclid algorithm

        public key: (b, n) -
            * compute n with the multiplication machine
        
        returns the steps list
        """
        machine_tapes = [self.n, self.phi, self.a]

        main_step = {
            "action": "main",
            "formula": "generation of the n (public key) and a (private key)",
            "tapes": copy.deepcopy(machine_tapes)
        }
        steps = []

        # Compute n = p * q
        mulMachine = Multiplication([self.p, self.q, self.n])
        subMachineStep = {
            "action": "submachine",
            "formula": "n = p * q",
            "tapes": copy.deepcopy(mulMachine.tapes)
        }
        mulSteps = mulMachine.runMachine()
        subMachineStep["steps"] = mulSteps
        steps.append(subMachineStep)

        # Compute phi(n) = (p - 1) * (q - 1)
        tapes = [self.p, self.q, self.phi]

        subMachineStep = {
            "action": "submachine",
            "formula": "phi(n) = (p - 1) * (q - 1)",
            "tapes": copy.deepcopy(tapes)
        }

        phiSteps = phiN(tapes)
        subMachineStep["steps"] = phiSteps
        
        steps.append(subMachineStep)

        # Compute a using the Euclid algorithm
        euclidMachine = Euclid([self.phi, self.b])
        subMachineStep = {
            "action": "submachine",
            "formula": "a = gcd(phi(n), b)",
            "tapes": copy.deepcopy(euclidMachine.tapes)
        }
        euclidSteps = euclidMachine.runMachine()
        subMachineStep["steps"] = euclidSteps
        steps.append(subMachineStep)

        # Set the private key 'a'
        self.a = euclidMachine.t()

        step = {
            "action" : "updateMachine",
            "tapes": machine_tapes
        }
        steps.append(step)

        main_step["steps"] = steps
        # Return the object with action, formula, and steps
        return main_step

    def getKeyGenerationSteps(self):
        """
        Retrieves the key generation steps and resets the attribute.
        """
        steps = self._key_generation_steps  # Retrieve the steps
        self._key_generation_steps = None  # Reset the attribute
        return steps

    def encrypt(self, x: int):
        xList = decimalToBinaryList(x)

        square = Squere([xList, self.b, self.n])
        square.runMachine()
        print(f"The encrypted value of {x} is: {binaryToDecimal(square.result())}")

    

    def decrypt(self, y: int):
        yList = decimalToBinaryList(y)

        def xi(v: list):
            """
            v = p or q
            compute x1 or x2 for the crt
                * x = y % v
                * b = a % (v-1)
                * n = v
                * compute x^b mod n = (y mod v)^(a mod (v-1)) % v
                * 
            """
            # x = y % v
            xMachine = Division([yList, v]) 
            xMachine.runMachine()
            x = xMachine.getRemainder()

            # minus = v-1
            minus = []
            Subtraction([v, [1], minus ]).runMachine()

            # b = a % (v-1)
            bMachine = Division([self.a, minus])
            bMachine.runMachine()
            b = bMachine.getRemainder()

            # result = (x^b)% v
            square = Squere([x, b, v])
            square.runMachine()
            result = square.result()

            return result

        x1 = xi(self.p)
        x2 = xi(self.q)

        crtMachine = Crt([x1, x2, self.p, self.q])
        crtMachine.runMachine()

        x = crtMachine.getX()

        print(f"The decrypted value of {y} is: {binaryToDecimal(x)}")
        

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