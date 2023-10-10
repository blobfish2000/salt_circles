import math

class V:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other): #addition
        if(type(other) == int or type(other) == float):
            return V(self.x + other, self.y + other)
        return V(self.x + other.x, self.y + other.y)

    def __radd__(self, other): #addition
        if(type(other) == int or type(other) == float):
            return V(self.x + other, self.y + other)
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

    def __lt__(self, other):
        return self.norm() < other.norm()

    def __le__(self, other):
        return self.norm() <= other.norm()

    def __gt__(self, other):
        return self.norm() > other.norm()

    def __ge__(self, other):
        return self.norm() >= other.norm()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return self.x != other.x or self.y != other.y
