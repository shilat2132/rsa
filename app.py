from basicMachines.mulMachine import mulPQ
from basicMachines.divMachine import DivMachine
from rsa.phi import phiN
from basicMachines.remainderMachine import remainderPQ


t1 = ["1", "1", "1", "1", "1", "1", "1"]
t2 = ["1", "1", "1", "1"]
#m = mulPQ([t1, t2, []])
#m.runMachine()
#print("the machine in the end: \n{m}".format(m=m))

# phiN(3, 5)

m = remainderPQ([t1, t2, []])
m.runMachine()

print("the machine in the end: \n{m}".format(m=m))


# t1 = ["1", "1", "1"]
# t2 = ["1", "1", "1", "1", "1"]
# m = mulPQ([t1, t2, []])
# m.runMachine()
# print("the machine in the end: \n{m}".format(m=m))

# phiN(3, 5)

t1 = ["_"]
t2 = ["_"]
d = DivMachine([t1, t2, []])
d.runMachine()
print("the machine in the end: \n{d}".format(d=d))
