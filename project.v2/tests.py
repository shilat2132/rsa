from operations.addition import Addition
from operations.multiplication import Multiplication
from operations.complement import complement
from operations.subtraction import Subtraction
from operations.division import Division

a = bin(4)[2:]
a = list(a)
a = [int(c) for c in a]
# a.insert(0, "-")


b = bin(3)[2:]
b = list(b)
b = [int(c) for c in b]
# b.insert(0, "-")


# add
# addMachine = Addition([a, b])
# addMachine.runMachine()
# print(addMachine)

# mul
mulMacine = Multiplication([a, b])
mulMacine.runMachine()
print(mulMacine)

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

