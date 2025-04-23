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




# p = decimalToBinaryList(127)
# q = decimalToBinaryList(191)
# b = decimalToBinaryList(47)

# r = RSA(p, q, b)
# # r.encrypt(2468)
# r.decrypt(10642)

# phi = phiN([decimalToBinaryList(103), decimalToBinaryList(101)])

# print(binaryToDecimal(phi))

a = decimalToBinaryList(5)
b = decimalToBinaryList(2)

# complement
# steps  = complement(a)
# print_steps(steps)

# print(a)

# div and remainder
# start = time.perf_counter()

divMachine = Division([a, b])
steps = divMachine.runMachine()
print_steps(steps)

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
# a = decimalToBinaryList(3120)
# b = decimalToBinaryList(17)
# start = time.perf_counter()
# e = Euclid([a, b])
# e.runMachine()
# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")
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
# x = decimalToBinaryList(6789)
# b = decimalToBinaryList(341)
# n = decimalToBinaryList(54321)

# start = time.perf_counter()
# squereMachine = Squere([x, b, n])
# squereMachine.runMachine()

# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")

# print(squereMachine)