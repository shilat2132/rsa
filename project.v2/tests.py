from turtle import st
from operations.addition import Addition
from operations.multiplication import Multiplication
from operations.complement import complement
from operations.subtraction import Subtraction
from operations.division import Division
from methods.squere import Squere
from RSA import RSA
import time
from operations.complement import complement

from methods.phi import phiN

from methods.euclidis import Euclid
from utils2 import binaryToDecimal, decimalToBinaryList, print_steps




p = decimalToBinaryList(3)
q = decimalToBinaryList(5)
b = decimalToBinaryList(3)

r= RSA(p, q, b)
# r.getKeyGenerationSteps()
# main_steps = r.encrypt(4)
# print_steps(main_steps["steps"])

main_steps = r.decrypt(4)
print_steps(main_steps["steps"])



# phi
# phi = []
# steps = phiN([decimalToBinaryList(2), decimalToBinaryList(3), phi])
# print_steps(steps)
# print(binaryToDecimal(phi))

# a = decimalToBinaryList(5)
# b = decimalToBinaryList(2)

# complement
# steps  = complement(a)
# print_steps(steps)

# print(a)

# div and remainder
# start = time.perf_counter()

# divMachine = Division([a, b])
# steps = divMachine.runMachine()
# print_steps(steps)

# print(divMachine)

# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")

# subtraction
# start = time.perf_counter()

# subMachine = Subtraction([a, b])
# subMachine.runMachine()
# end = time.perf_counter()

# print(subMachine)
# print(f"Time taken: {end - start} seconds")


# euclid
# a = decimalToBinaryList(7)
# b = decimalToBinaryList(3)
# e = Euclid([a, b])
# steps = e.runMachine()
# print_steps(steps)

# print(f"gcd =  {binaryToDecimal(e.d())}")
# print(f"s = {binaryToDecimal(e.s())}")
# print(f"t =  {binaryToDecimal(e.t())}")


# add
# a = decimalToBinaryList(2)
# b = decimalToBinaryList(3)
# addMachine = Addition([a, b])
# steps = addMachine.runMachine()
# print_steps(steps)

# mul
# a = decimalToBinaryList(2, True)
# b = decimalToBinaryList(2)

# start = time.perf_counter()
# mulMacine = Multiplication([a, b])
# steps = mulMacine.runMachine()
# print_steps(steps)

# print(mulMacine)

# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")
# print(mulMacine)

# complement
# complement(a)
# print(a)



# squere
# x = decimalToBinaryList(2)
# b = decimalToBinaryList(2)
# n = decimalToBinaryList(2)

# squereMachine = Squere([x, b, n])
# steps = squereMachine.runMachine()
# print_steps(steps)

# print(squereMachine.result())