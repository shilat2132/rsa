from basicMachines.mulMachine import mulPQ
from basicMachines.divMachine import divMachine
from rsa.phi import phiN
from basicMachines.subMachine import subMachine

# phi
# p = ["1", "1", "1"]
# q = ["1", "1", "1", "1", "1"]
# phiN(p, q)

# div
a = ["1" for i in range(3)]
b = ["1" for i in range(5)]
a.insert(0, "-")
b.insert(0, "-")

subMachine(a, b)
print("the result of subtraction: {a}".format(a=a))