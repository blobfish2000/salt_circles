import random
from render import *
import math

class V:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): #addition
        return V(self.x + other.x, self.y + other.y)

    def __sub__(self, other): #subtraction
        return V(self.x - other.x, self.y - other.y)

    def __mul__(self, other): #scalar multiplication and dot product
        if isinstance(other, V):
            return self.x * other.x + self.y * other.y
        else:
            return V(self.x * other, self.y * other)

    def __rmul__(self, other): #scalar multiplication
        return V(self.x * other, self.y * other)

    def __truediv__(self, other): #scalar division
        return V(self.x / other, self.y / other)

    def __neg__(self): #negation
        return V(-self.x, -self.y)

    def __repr__(self):
        return "V({}, {})".format(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        return self / self.norm()

    def rotate(self, angle):
        return V(self.x * math.cos(angle) - self.y * math.sin(angle), self.x * math.sin(angle) + self.y * math.cos(angle))

class Structure:
    def distance_to(self, point):
        #distance to edge from point (naively just the norm of the difference)
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2) - self.radius

    def render_in(self, scene):
        #make the relevant graphics primitives and add them to the scene
        pass

class Circle(Structure):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render_in(self, scene):
        scene.add_circle(self.x, self.y, self.radius, Material("#"))
