from basicMachines.mulMachine import mulMachine
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine
from tm import Tm
from basicMachines.remainderMachine import remainderMachine
from rsa.Euclid import Euclid
from rsa.encryption.binaryMachine import binary
from basicMachines.powerMachine import powerMachine
from utils import unaryToDecimal

a = ["1" for i in range(7)]
b = ["1" for i in range(3)]
# a.insert(0, "-")


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

# eu = Euclid([a, b])
# config = eu.runEuclidAbstract()
# print(f"the result of d: {eu.d()}. the number in this tape is: {unaryToDecimal(eu.d())}")
# print(f"the result of s: {eu.s()}. the number in this tape is: {unaryToDecimal(eu.s())}")
# print(f"the result of t: {eu.t()}. the number in this tape is: {unaryToDecimal(eu.t())}")


# phi
# result = []
# config = phiN([a,b, result])
# print(f"phi of n: {result}. the number in this tape is: {unaryToDecimal(result)}")

# div
# d= divMachine([a, b])
# config =  d.runMachine()
# print("the machine of division: {d}".format(d=d))


# sub
# config = subMachine(a, b)
# print("the result of subtraction: {a}".format(a=a))


# mul
# m= mulMachine([a, b])
# config = m.runMachine()
# print("the machine of multiplication: {m}".format(m=m))

# print(config)
