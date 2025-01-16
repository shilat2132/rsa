from basicMachines.mulMachine import mulMachine
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine
from tm import Tm
from basicMachines.remainderMachine import remainderPQ
from rsa.gcd import Gcd

a = ["1" for i in range(111)]
b = ["1" for i in range(30)]

# remainder
# m = remainderPQ([a, b])
# m.runMachine()
# print("the machine in the end: \n{m}".format(m=m))


# gcd

gc = Gcd([a, b])
gc.runGcdAbstract()
print("the result of gcd: {d}".format(d= gc.d()))
print("s=  {s}".format(s= gc.s()))
print("t=  {t}".format(t= gc.t()))

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
# m= mulMachine([a, b])
# m.runMachine()
# print("the machine of multiplication: {m}".format(m=m))

