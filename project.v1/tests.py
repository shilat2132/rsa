from turtle import st
from basicMachines.mulMachine import mulMachine
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine
from tm import Tm
from basicMachines.remainderMachine import remainderMachine
from rsa.Euclid import Euclid
from rsa.squere.binaryMachine import binary
from rsa.squere.square import SquereM
from utils import unaryToDecimal
import time



# a = "1100101"
# a = list(a)
# b = "1100101"
# b = list(b)



# a = ["1" for i in range(500)]
# a = bin(1228)[2:]
# a = list(a)
# b = ["1" for i in range(101)]
# a = binary(a)

# mul binary
# mulBinaryMachine = MulBinary([a, a.copy()])
# mulBinaryMachine.runMachine()
# print(mulBinaryMachine.tapes[2])

# add binary
# addBinMachine = AddBinary([a, b])
# addBinMachine.runMachine()
# print(addBinMachine)


a = ["1" for i in range(16)]
b = ["1" for i in range(500)]
# a.insert(0, "-")

# x = ["1" for i in range(101)]
# n = ["1" for i in range(34)]
# squareMachine = SquereM([x, b, n])
# squareMachine.runMachine()
# result = squareMachine.result()

# power
# pow, config = powerMachine(a, b)
# print(f"a^b: \n {pow} \n the number in this tape is: {unaryToDecimal(pow)}")

# binary
# bin, config = binary(a)
# print(f"the binary number: {bin}")

# remainder
# m = remainderMachine([a, b])
# config = m.runMachine()
# print(f"the result of the remainder: \n{m.tapes[2]}")


# Euclid

# start = time.perf_counter()
# eu = Euclid([a, b])
# config = eu.runEuclidAbstract()
# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")
# print(f"gcd =  {unaryToDecimal(eu.d())}")
# print(f"s = {unaryToDecimal(eu.s())}")
# print(f"t =  {unaryToDecimal(eu.t())}")

# a.insert(0, "-")
# b.insert(0, "-")

# phi
# result = []
# config = phiN([a,b, result])
# print(f"phi of n: {result}. the number in this tape is: {unaryToDecimal(result)}")

# div
# start = time.perf_counter()
# d= divMachine([a, b])
# config =  d.runMachine()

# end = time.perf_counter()
# print(f"Time taken: {end - start} seconds")
# print("the machine of division: {d}".format(d=d))

# copy
# Tm.copyTape(a, b)
# print(a, b)

# sub
# start = time.perf_counter()

# config = subMachine(a, b)
# end = time.perf_counter()
# print(end - start)




# mul

start = time.perf_counter()
m= mulMachine([a, b])
config = m.runMachine()
end = time.perf_counter()
print(f"Time taken: {end - start} seconds")
# print("the machine of multiplication: {m}".format(m=m))

# print(config)
