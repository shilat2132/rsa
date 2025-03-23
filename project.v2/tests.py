from operations.addition import Addition
from operations.multiplication import Multiplication
from operations.complement import complement
from operations.subtraction import Subtraction
from operations.division import Division
from methods.squere import Squere
from RSA import RSA

from methods.phi import phiN

from methods.euclidis import Euclid
from utils2 import binaryToDecimal


def decimalToBinaryList(num, minus = False):
    a = bin(num)[2:]
    a = list(a)
    a = [int(c) for c in a]
    if minus:
        a.insert(0, "-")
    
    return a

p = decimalToBinaryList(37)
q = decimalToBinaryList(41)
b = decimalToBinaryList(31)

r = RSA(p, q, b)
print(r)

# phi = phiN([decimalToBinaryList(103), decimalToBinaryList(101)])

# print(binaryToDecimal(phi))

a = decimalToBinaryList(13, True)
b = decimalToBinaryList(26)

# div and remainder
# divMachine = Division([a, b])
# divMachine.runMachine()
# print(divMachine)

# subtraction
# subMachine = Subtraction([a, b])
# subMachine.runMachine()
# print(subMachine)

# e = Euclid([a, b])
# e.runMachine()
# print(f"gcd =  {binaryToDecimal(e.d())}")
# print(f"s = {binaryToDecimal(e.s())}")
# print(f"t =  {binaryToDecimal(e.t())}")


# add
# addMachine = Addition([a, b])
# addMachine.runMachine()
# print(addMachine)

# mul
# a = decimalToBinaryList(13)
# b = decimalToBinaryList(2, True)

# mulMacine = Multiplication([a, b])
# mulMacine.runMachine()
# print(mulMacine)

# complement
# complement(a)
# print(a)







# squere
# x = decimalToBinaryList(6789)
# b = decimalToBinaryList(34)
# n = decimalToBinaryList(54321)

# squereMachine = Squere([x, b, n])
# squereMachine.runMachine()
# print(squereMachine)