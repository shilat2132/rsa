from calendar import c
from math import e
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

    def __init__(self, p: list = None, q: list = None, b: list = None, n: list = None, a: list = None):
        """
        Holds the public and private keys of the RSA algorithm.
        supports constructing the object with either:
        - (p, q, b) for generating the keys
        - (b, n) for encrypting
        - (a, p, q) for decrypting
        """

      

        self.n = []
        self.phi = []
        self.a = []



        if p is not None and q is not None and b is not None:
            self.b = b
            self.p = p
            self.q = q
            # Store the key generation steps temporarily
            self._key_generation_steps = self.keyGeneration()
        
        elif b is not None and n is not None:
            self.b = b
            self.n = n
        
        elif a is not None and p is not None and q is not None:
            self.a = a
            self.p = p
            self.q = q

        else:
            raise ValueError("Invalid parameters: either (p, q, b) for generation or (b, n) for encryption or (a, p, q) for decryption are required.")


    def keyGeneration(self):
        """
        private key: (p, q, a) - 
            * compute phi = (p-1)(q-1)
            * compute a with the Euclid algorithm

        public key: (b, n) -
            * compute n with the multiplication machine
        
        returns the main step object
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

    def getKeyGeneration(self):
        """
        Retrieves the key generation steps and resets the attribute. Also returns n and a.
        """
        steps = self._key_generation_steps  # Retrieve the steps
        self._key_generation_steps = None  # Reset the attribute
        return steps, self.n, self.a

    def encrypt(self, x: int):
        """
        Encrypts the given integer x using the RSA algorithm.
        Builds a main step object to log the encryption process.
        """
        steps = []

        
        # Convert x to binary list
        xList = decimalToBinaryList(x)
        machine_tapes = [xList, self.b, self.n, ["_"]]
        main_step = {
            "action": "main",
            "formula":  f"Encrypt {x}",
            "tapes": copy.deepcopy(machine_tapes)
        }

        # Perform squaring operation: y = x^b % n
        square = Squere([xList, self.b, self.n])
        subMachineStep = {
            "action": "submachine",
            "formula": "y = x^b % n",
            "tapes": copy.deepcopy(square.tapes)
        }
        squareSteps = square.runMachine()
        subMachineStep["steps"] = squareSteps
        steps.append(subMachineStep)

        # Retrieve the result of the encryption
        y = square.result()
        encryptedValue = binaryToDecimal(y)

        updateTapeStep = {
            "action": "updateTape",
            "tape_index": 3, 
            "tape": y.copy()
        }
        steps.append(updateTapeStep)

        main_step["steps"] = steps

        print(f"The encrypted value of {x} is: {encryptedValue}")
        return main_step

    def decrypt(self, y: int):
        """
        Decrypts the given integer y.
        returns a main step object.
        """
        steps = []

        # Convert y to binary list
        yList = decimalToBinaryList(y)

        machine_tapes = [yList, ["_"]]
        main_step = {
            "action": "main",
            "formula": f"Decrypt {y}",
            "tapes": copy.deepcopy(machine_tapes)
        }

        def xi(v: list):
            """
             v = p or q
                Compute x1 or x2 for the CRT:
                * x = y % v
                * b = a % (v-1)
                * n = v
                * compute x^b mod n = (y mod v)^(a mod (v-1)) % v
                - returns the result and the steps of the submachine.
            """
            xi_steps = []

            # x = y % v
            xMachine = Division([yList, v])
            subMachineStep = {
                "action": "submachine",
                "formula": "Compute y % v (v is either p or q)",
                "tapes": copy.deepcopy(xMachine.tapes)
            }
            subMachineStep["steps"] = xMachine.runMachine()
            xi_steps.append(subMachineStep)
            x = xMachine.getRemainder()

            # minus = v - 1
            minus = []
            subtractionMachine = Subtraction([v, [1], minus])
            subMachineStep = {
                "action": "submachine",
                "formula": "Compute v - 1 = p - 1 or q - 1",
                "tapes": copy.deepcopy(subtractionMachine.tapes)
            }
            subMachineStep["steps"] = subtractionMachine.runMachine()
            xi_steps.append(subMachineStep)

            # b = a % (v - 1)
            bMachine = Division([self.a, minus])
            subMachineStep = {
                "action": "submachine",
                "formula": "b = a % (v - 1)",
                "tapes": copy.deepcopy(bMachine.tapes)
            }
            subMachineStep["steps"] = bMachine.runMachine()
            xi_steps.append(subMachineStep)
            b = bMachine.getRemainder()

            # result = (x^b) % v
            square = Squere([x, b, v])
            subMachineStep = {
                "action": "submachine",
                "formula": "result = (y%v)^(a%(v-1)) % v",
                "tapes": copy.deepcopy(square.tapes)
            }
            subMachineStep["steps"] = square.runMachine()
            xi_steps.append(subMachineStep)
            result = square.result()

            return result, xi_steps

        # Compute x1 and x2
        x1, x1_steps = xi(self.p)
        steps.extend(x1_steps)

        x2, x2_steps = xi(self.q)
        steps.extend(x2_steps)

        # Perform CRT to combine x1 and x2
        crtMachine = Crt([x1, x2, self.p, self.q])
        crtStep = crtMachine.runMachine()  # The CRT machine returns its submachine object
        steps.append(crtStep)

        # Retrieve the decrypted value
        x = crtMachine.getX()
        decryptedValue = binaryToDecimal(x)

        updateTapeStep = {
            "action": "updateTape",
            "tape_index": 1,  
            "tape": x.copy()
        }
        steps.append(updateTapeStep)

        main_step["steps"] = steps

        print(f"The decrypted value of {y} is: {decryptedValue}")
        return main_step

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