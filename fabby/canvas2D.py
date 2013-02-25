import numpy
import gcode

class Canvas2DConfig(object):
    def __init__(self,
                 distance_to_extrude_ratio = 1.0/14.0,
                 speed = 540.0,
                 extrude_start_length = 1.0,
                 print_width = 0.6,
                 layer_height = 0.3):
        self.distance_to_extrude_ratio = distance_to_extrude_ratio
        self.speed = speed
        self.extrude_start_length = extrude_start_length
        self.print_width = print_width
        self.layer_height = layer_height


class Canvas2D(object):
    def __init__(self, producer, config):
        self.producer = producer
        self.config = config
        self.last_point = None
        self.last_extrude = None

    def transform(self, point):
        return point + numpy.array([100, 100])

    def addOp(self, op):
        self.producer.addOp(op)

    def reset(self):
        self.last_extrude = None
        self.last_point = None

        rst = gcode.GCodeStartDrawOperation(self.config.speed,
                                            self.config.extrude_start_length)
        self.addOp(rst)

    def move_(self, point, extrude = True):
        point = self.transform(point)
        e = 0
        if self.last_extrude is not None:
            if extrude:
                d = numpy.linalg.norm(point - self.last_point)
                e = self.last_extrude + d * self.config.distance_to_extrude_ratio
                move = gcode.GCodeMove(x = point[0], y = point[1], e = e)
            else:
                e = self.last_extrude
                move = gcode.GCodeMove(x = point[0], y = point[1])

            self.addOp(move)
        else:
            self.reset()
            move = gcode.GCodeMove(x = point[0], y = point[1])
            self.addOp(move)

        self.last_extrude = e
        self.last_point = point

    def drawTo(self, point):
        return self.move_(point, extrude = True)
    
    def move(self, point):
        return self.move_(point, extrude = False)

