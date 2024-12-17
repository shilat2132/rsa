from basicMachines.mulMachine import mulPQ

t1 = ["1", "1", "1"]
t2 = ["1", "1", "1", "1", "1"]
m = mulPQ([t1, t2, []], "start")
m.runMachine()
print("the machine in the end: \n{m}".format(m=m))