class GCodeProducer(object):
    def __init__(self):
        self.operations = []

    def addOp(self, op):
        self.operations += [op]

    def __repr__(self):
        return "\n".join([str(op) for op in self.operations])
