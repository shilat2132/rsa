 def keyGeneration(self):
        phiN([self.p, self.q, self.phi])
        Multiplication([self.p, self.q, self.n]).runMachine()
        euclidMachine = Euclid([self.phi, self.b])
        euclidMachine.runMachine()
        self.a = euclidMachine.t()