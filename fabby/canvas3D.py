import canvas2D
import gcode

class Canvas3DConfig(object):
    def __init__(self, first_layer_config, normal_layer_config, zmax):
        self.first_layer_config = first_layer_config
        self.normal_layer_config = normal_layer_config
        self.zmax = zmax

    def getLayerConfig(self, index):
        if index == 0:
            return self.first_layer_config
        else:
            return self.normal_layer_config
        
class Canvas3D(object):
    def __init__(self, producer, config):
        self.producer = producer
        self.config = config
        self.shapes = []        

    def addShape(self, shape):
        self.shapes += [shape]

    def addOp(self, op):
        self.producer.addOp(op)

    def draw(self):
        z = 0.0
        layerIndex = 0
        while z < self.config.zmax:
            config2D = self.config.getLayerConfig(layerIndex)
            canv2D = canvas2D.Canvas2D(self.producer, config2D)
            z += config2D.layer_height
            

            moved = False
#            G1 Z0.400 F7800.000
            for s in self.shapes:
                if s.hasintersect(z):
                    if not moved:
                        zmove = gcode.GCodeMove(z = z)
                        self.addOp(zmove)
                        extrudeReset = gcode.GCodeExtrudeReset()
                        self.addOp(extrudeReset)                        
                        
                        moved = True                        
                    s.draw(canv2D, z)
            
            layerIndex += 1
        print "Printed %d layers" % layerIndex
        
    
