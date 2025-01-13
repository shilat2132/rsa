from basicMachines.mulMachine import mulMachine
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine
from tm import Tm
from basicMachines.remainderMachine import remainderMachine
from rsa.Euclid import Euclid
from rsa.encryption.binaryMachine import binary

a = ["1" for i in range(6)]
b = ["1" for i in range(26)]
# a.insert(0, "-")


# binary
bin = binary(a)
print(f"the binary number: {bin}")

# remainder
# m = remainderMachine([a, b])
# m.runMachine()
# print("the machine in the end: \n{m}".format(m=m))


# Euclid

# eu = Euclid([a, b])
# eu.runEuclidAbstract()
# print("the result of d: {d}".format(d= eu.d()))
# print("the result of t: {t}".format(t= eu.t()))
# print("the result of s: {s}".format(s= eu.s()))


# phi
# p = ["1", "1", "1"]
# q = ["1", "1", "1", "1", "1"]
# phiN(p, q)

# div
# d= divMachine([a, b])
# d.runMachine()
# print("the machine of division: {d}".format(d=d))


# sub
# subMachine(a, b)
# print("the result of subtraction: {a}".format(a=a))


# mul
# m= mulMachine([a, b])
# m.runMachine()
# print("the machine of multiplication: {m}".format(m=m))
