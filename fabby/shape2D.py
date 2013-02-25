import math
import numpy

class Shape2DProducer(object):
    def __init__(self, canvas2D):
        self.canvas = canvas2D

    def add_to_producer(self, producer):
        pass


class Circle2DProducer(Shape2DProducer):
    def __init__(self, canvas, center, radius, nsides = 32):
        super(Circle2DProducer, self).__init__(canvas)
        self.center = center
        self.radius = radius
        self.nsides = nsides

    def draw(self):
        fullCircle = 2 * math.pi

        for i in range(self.nsides + 1):

            angle = i * fullCircle / self.nsides
            x = math.cos(angle) * self.radius + self.center[0]
            y = math.sin(angle) * self.radius + self.center[0]
            point = numpy.array([x, y])
            if i == 0:
                self.canvas.move(point)
            else:                
                self.canvas.drawTo(point)

class Ring2DProducer(Shape2DProducer):
    # overlap measure the amount of overlap between consecutive circles
    def __init__(self, canvas, center, inner_radius, outer_radius, nsides = 36, overlap = 0.0, reverse = False):
        super(Ring2DProducer, self).__init__(canvas)
        self.center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.nsides = nsides
        self.overlap = overlap
        self.reverse = reverse
        if (self.outer_radius < self.inner_radius):
            raise "InvalidDisc radius: outer = %f < inner = %f" % (outer_radius, inner_radius)
        
    def draw(self):
        width = self.canvas.config.print_width
        # as we have a ngon, we have to measure the width in the middle of each side
        angle = 2 * math.pi / self.nsides / 2
        radiusDiff = (self.outer_radius - self.inner_radius) * math.cos(angle)
        sliceCount = int(round((radiusDiff * (1.0 + self.overlap)) / width))
        maxRadius = self.outer_radius - width / 2.0
        minRadius = self.inner_radius + width / 2.0
        radiusIncrement = (self.outer_radius - self.inner_radius) / sliceCount
        rge = [i for i in range(sliceCount)]
        if self.reverse:
            rge.reverse()
        for i in rge:
            radius = minRadius + radiusIncrement * i
            circle = Circle2DProducer(self.canvas, self.center, radius, self.nsides)
            circle.draw()
