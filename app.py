from basicMachines.mulMachine import mulMachine
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine
from tm import Tm


a = ["1" for i in range(4)]
b = ["1" for i in range(2)]
# a.insert(0, "-")
# b.insert(0, "-")

# phi
# p = ["1", "1", "1"]
# q = ["1", "1", "1", "1", "1"]
# phiN(p, q)

# div
# d= divMachine([a, b])
# d.runMachine()
# print("the machine of division: {d}".format(d=d))

# copy
# Tm.copyTape(a, b)
# print(a, b)

# sub
# subMachine(a, b)
# print("the result of subtraction: {a}".format(a=a))


# mul
m= mulMachine([a, b])
m.runMachine()
print("the machine of multiplication: {m}".format(m=m))