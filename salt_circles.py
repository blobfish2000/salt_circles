import random
import math
import time


class Rune:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bounds()

    def bounds(self):
        self.x_bounds = [x,x]
        self.y_bounds = [y,y]

    def render(self,x,y):
        return False

class Circle(Rune):
    def __init__(self, x, y, radius, width = 0.75, edge = "x", fill = "_"):
        self.radius = radius
        Rune.__init__(self,x,y)
        self.width = width
        self.bounds()
        self.edge = edge
        self.fill = fill

    def bounds(self):
        self.x_bounds = [self.x-self.radius, self.x+self.radius]
        self.y_bounds = [self.y-self.radius, self.y+self.radius]

    def render(self,x,y):
        if x == self.x and y == self.y:
            return False
        x_distance = x-self.x
        y_distance = y-self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        deviation = distance - self.radius
        if abs(deviation) <= self.width/2:
            return self.edge
        elif distance <= self.radius:
            return self.fill
        else:
            return False

    def __repr__(self):
        return(f"<X:{self.x}, Y:{self.y}, Radius: {self.radius}, Bounds:{self.x_bounds, self.y_bounds}>")

class StarredCircle(Circle):

    def point_on_line(x1, y1, x2, y2, px, py, width=0.5):
        # project 1p onto 12

        AB = (x2-x1, y2-y1)
        AP = (px-x1, py-y1)

        projection_x = AB[0] * (AB[0]*AP[0] + AB[1]*AP[1]) / (AB[0]**2 + AB[1]**2)
        projection_y = AB[1] * (AB[0]*AP[0] + AB[1]*AP[1]) / (AB[0]**2 + AB[1]**2)

        deviation_x = AP[0] - projection_x
        deviation_y = AP[1] - projection_y

        deviation = math.sqrt(deviation_x**2 + deviation_y**2)

        between = (projection_x >= 0 and projection_x <= AB[0]) or (projection_x <= 0 and projection_x >= AB[0])
        if projection_x == 0:
            between = (projection_y >= 0 and projection_y <= AB[1]) or (projection_y <= 0 and projection_y >= AB[1])

        if deviation <= width and between:
            return True
        elif deviation <= width*2 and between:
            if random.random() < 0.5:
                return True
        else:
            return False

    
    def __init__(self, x, y, radius, width = 0.75, edge = "x", fill = "_", star = "@", inverted = False):
        Circle.__init__(self,x,y,radius, edge = edge, fill = fill)
        self.star = star
        self.inverted = inverted

    def render(self,x,y):
        if x == self.x and y == self.y:
            return False
        x_distance = x-self.x
        y_distance = y-self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        deviation = distance - self.radius

        star_points = []
        for i in range(0,5):
            if not self.inverted:
                angle = 2*math.pi*i/5 - math.pi/2
            else:
                angle = 2*math.pi*i/5 + math.pi/2
            star_points.append((self.x + self.radius*math.cos(angle), self.y + self.radius*math.sin(angle)))

        star_points.append(star_points[0])
        star_points.append(star_points[1])
        for i in range(0,5):
            if StarredCircle.point_on_line(star_points[i][0], star_points[i][1], star_points[i+2][0], star_points[i+2][1], x, y, width = 0.25):
                return self.star

        if abs(deviation) <= self.width/2:
            return self.edge
        elif distance <= self.radius:
            return self.fill
        else:
            return False


class Force():
    def __init__(self, function):
        self.function = function

    def __call__(self, a, b):
        return self.function(a,b)

def edge_attraction(a,b):
    if not hasattr(a, "radius") or not hasattr(b, "radius"):
        return [0,0]
    #force on a from b
    x_distance = b.x - a.x
    y_distance = b.y - a.y
    #vector from a to b
    distance = math.sqrt(x_distance**2 + y_distance**2)
    if a.radius < 4:
        deviation = abs(distance - b.radius)
    else:
        deviation = abs(distance - (a.radius + b.radius))

    delta = [x_distance, y_distance]
    delta = [d/((deviation+4)**2) for d in delta]
    if a.radius < 4:
        distance = distance + a.radius
    if distance < a.radius + b.radius:
        return [-delta[0], -delta[1]]
    else:
        return delta

def strong_centration(a,b):
    if not hasattr(a, "radius") or not hasattr(b, "radius"):
        return [0,0]
    x_distance = b.x - a.x
    y_distance = b.y - a.y
    #vector from a to b
    distance = math.sqrt(x_distance**2 + y_distance**2)
    radius_difference = abs(a.radius - b.radius)
    if radius_difference > 1 and radius_difference < 8 and distance < 5:
        delta = [x_distance, y_distance] + [x_distance/(distance+1), y_distance/(distance+1)]
        return delta
    else:
        return [0,0]

        
edge_attraction = Force(edge_attraction)
strong_centration = Force(strong_centration)
    
def render(runes):
    x_min = round(min([r.x_bounds[0] for r in runes]) - 0.5)
    x_max = round(max([r.x_bounds[1] for r in runes]) + 0.5)
    y_min = round(min([r.y_bounds[0] for r in runes]) - 0.5)
    y_max = round(max([r.y_bounds[1] for r in runes]) + 0.5)

    buffer = ""
    character_heirarchy = ["@","x","_", ".", " "]

    for y in range(y_min, y_max+1):
        for x in range(x_min*2, (x_max+1)*2):
            x = x/2
            character_candidates = [" "]
            for rune in runes:
                result = rune.render(x,y)
                if result:
                    character_candidates.append(result)

            character = filter(lambda x: x in character_candidates, character_heirarchy).__next__()
            for c in character_candidates:
                if c not in character_heirarchy:
                    character = c
                    
            if character == "_":
                character = " "
            buffer += character
        buffer += "\n"

    return buffer

def simulate(runes, forces, iterations = 1000, precision = 0.01):
    for i in range(iterations):
        for rune in runes:
            for force in forces:
                comm_force = [0,0]
                for other_rune in runes:
                    if rune != other_rune:
                        delta = force(rune, other_rune)
                        comm_force[0] += delta[0]
                        comm_force[1] += delta[1]

                rune.x += comm_force[0] * precision
                rune.y += comm_force[1] * precision
                rune.bounds()
        if i % int(iterations/10) == 0:
            print(render(runes))
            time.sleep(0.2)


if __name__ == "__main__":
    runes = []
    for _ in range(5):
        if random.random() < 0.5:
            rune = Circle(random.randint(-15,15),random.randint(-15,15),random.randint(2,8))
            runes.append(rune)
        else:
            rune = Circle(random.randint(-15,15),random.randint(-15,15),random.randint(2,8), fill = ".")
            runes.append(rune)
    rune = StarredCircle(random.randint(-15,15),random.randint(-15,15),random.randint(8,14),inverted = random.random() < 0.5)
    runes.append(rune)

    print(render(runes))
    simulate(runes, [edge_attraction, strong_centration], iterations = 10000, precision = 0.01)
