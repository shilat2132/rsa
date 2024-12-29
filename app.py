from basicMachines.mulMachine import mulPQ
from rsa.phi import phiN


t1 = ["1", "1", "1"]
t2 = ["1", "1", "1", "1", "1"]
m = mulPQ([t1, t2, []])
m.runMachine()
print("the machine in the end: \n{m}".format(m=m))

# phiN(3, 5)