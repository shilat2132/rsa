from basicMachines.mulMachine import mulPQ
from rsa.phi import phiN
from basicMachines.remainderMachine import remainder


t1 = ["1", "1", "1"]
t2 = ["1", "1", "1", "1", "1"]
m = mulPQ([t1, t2, []])
m.runMachine()
print("the machine in the end: \n{m}".format(m=m))

# phiN(3, 5)

rm = remainder([t1, t2, []])
rm.runMachine

print("the machine in the end: \n{rm}".format(m=rm))