from operations.addition import Addition
from operations.multiplication import Multiplication
from operations.complement import complement
from operations.subtraction import Subtraction
from operations.division import Division
from methods.squere import Squere


def decimalToBinaryList(num, minus = False):
    a = bin(num)[2:]
    a = list(a)
    a = [int(c) for c in a]
    if minus:
        a.insert(0, "-")
    
    return a


# a = decimalToBinaryList(20)
# b = decimalToBinaryList(16)


# add
# addMachine = Addition([a, b])
# addMachine.runMachine()
# print(addMachine)

# mul
# mulMacine = Multiplication([a, b])
# mulMacine.runMachine()
# print(mulMacine)

# complement
# complement(a)
# print(a)

# subtraction
# subMachine = Subtraction([a, b])
# subMachine.runMachine()
# print(subMachine)


# div and remainder
# divMachine = Division([a, b])
# divMachine.runMachine()
# print(divMachine)


# squere
x = decimalToBinaryList(6789)
b = decimalToBinaryList(34)
n = decimalToBinaryList(54321)

squereMachine = Squere([x, b, n])
squereMachine.runMachine()
print(squereMachine)