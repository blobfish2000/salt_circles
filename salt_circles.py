import random
import math


class Rune:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_bounds = [x,x]
        self.y_bounds = [y,y]

    def render(self,x,y):
        return False

class Circle(Rune):
    def __init__(self, x, y, radius, width = 0.5):
        Rune.__init__(self,x,y)
        self.x_bounds = [x-radius, x+radius]
        self.y_bounds = [y-radius, y+radius]
        self.radius = radius
        self.width = width

    def render(self,x,y):
        if x == self.x and y == self.y:
            return False
        x_distance = x-self.x
        y_distance = y-self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        deviation = distance - self.radius
        if abs(deviation) <= self.width/2:
            return "x"
        else:
            return False

    def __repr__(self):
        return(f"<X:{self.x}, Y:{self.y}, Radius: {self.radius}, Bounds:{self.x_bounds, self.y_bounds}>")
    
def render(runes):
    x_min = min([r.x_bounds[0] for r in runes])
    x_max = max([r.x_bounds[1] for r in runes])
    y_min = min([r.y_bounds[0] for r in runes])
    y_max = max([r.y_bounds[1] for r in runes])

    buffer = ""

    for y in range(y_min, y_max+1):
        for x in range(x_min*2, (x_max+1)*2):
            x = x/2
            character = " "
            for rune in runes:
                result = rune.render(x,y)
                if result:
                    character = result
            buffer += character
        buffer += "\n"

    return buffer


if __name__ == "__main__":
    runes = []
    for _ in range(4):
        rune = Circle(random.randint(-15,15),random.randint(-15,15),random.randint(3,8))
        runes.append(rune)
        
    print(render(runes))
