
class GCodeParam(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name + str(self.value)


class GCodeOperation(object):
    def __init__(self, opName, parameters):
        self.opName = opName
        self.parameters = parameters

    def __repr__(self):
        parts = [self.opName] + [str(p) for p in self.parameters]
        return " ".join(parts)


class GCodeStartDrawOperation(GCodeOperation):
    def __init__(self, speed, extrude):
        super(GCodeStartDrawOperation, self).__init__("G1",
                                                      [GCodeParam("F", speed),
                                                       GCodeParam("E", extrude)])

class GCodeMove(GCodeOperation):
    def __init__(self, **kwargs):
        parameters = []
        for arg in "xyze":
            if arg in kwargs and kwargs[arg] != None:
                parameters += [GCodeParam(arg.upper(), kwargs[arg])]
                
        super(GCodeMove, self).__init__("G1", parameters)


class GCodeExtrudeReset(GCodeOperation):
    def __init__(self, **kwargs):
        super(GCodeExtrudeReset, self).__init__("G92", [GCodeParam("E", 0)])


