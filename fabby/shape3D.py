import shape2D

class Shape3DProducer(object):
    def __init__(self, canvas3D):
        self.canvas = canvas3D
        canvas3D.addShape(self)
        
    def hasintersect(self, z):
        return False
    
    def draw(self, z):
        pass
            
class Tube3DProducer(Shape3DProducer):
    # overlap measure the amount of overlap between consecutive circles
    def __init__(self, canvas, center, inner_radius, outer_radius, zmin, zmax, nsides = 36, overlap = 0.0):
        super(Tube3DProducer, self).__init__(canvas)
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.zmin = zmin
        self.zmax = zmax
        self.nsides = nsides
        self.overlap = overlap
        
        if (self.outer_radius < self.inner_radius):
            raise "InvalidDisc radius: outer = %f < inner = %f" % (outer_radius, inner_radius)
        # Alternate layers from inbound to outbound
        self.reverse = False

        
    def hasintersect(self, z):
        return z >= self.zmin and z <= self.zmax

    def draw(self, canvas2D, z):
        ring2D = shape2D.Ring2DProducer(canvas2D,
                                        self.center,
                                        self.inner_radius, self.outer_radius,
                                        self.nsides,
                                        self.overlap,
                                        reverse = self.reverse)
        self.reverse = not self.reverse
        ring2D.draw()
        
