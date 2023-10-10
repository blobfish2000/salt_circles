import random
from render import *
from vector import V
import time

class Structure:
    def __init__(self, location):
        self.location = location

    def tangent_vector(self, point):
        #vector to edge from point
        return V(0,0)

    def distance_to(self, point):
        #distance to edge from point
        return self.tangent_vector(point).norm()

    def render_in(self, scene):
        #make the relevant graphics primitives and add them to the scene
        pass

class CircleS(Structure):
    def __init__(self, location, radius):
        super().__init__(location)
        self.radius = radius

    def render_in(self, scene, material, fill_material=None):
        circle = Circle(self.location.x, self.location.y, self.radius, material, fill_material)
        scene.objects.append(circle)

    def tangent_vector(self, point):
        naive = self.location - point
        length = naive.norm()
        if length == 0:
            return V(self.radius, 0)
        return naive.normalized()*(length-self.radius)

    def distance_to(self, point):
        return self.tangent_vector(point).norm()

class LineS(Structure):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        super().__init__((start+end)/2)

    def render_in(self, scene, material):
        line = Line(self.start.x, self.start.y, self.end.x, self.end.y, material)
        scene.objects.append(line)

    def tangent_vector(self, point):
        #vector to edge from point
        line_vector = self.start - self.end
        point_vector = self.start - point
        projection = point_vector * line_vector.normalized()
        if projection < 0:
            return point_vector
        elif projection > line_vector.norm():
            return self.end - point
        else:
            return point_vector - line_vector.normalized()*projection

class PolygonS(Structure):
    def __init__(self, points):
        self.points = points
        print(points)
        super().__init__(sum(points)/len(points))

    def render_in(self, scene, material, fill_material=None):
        polygon = Polygon([(p.x, p.y) for p in self.points], material, fill_material)
        scene.objects.append(polygon)

    def tangent_vector(self, point):
        final = V(float("inf"), float("inf"))
        for i in range(len(self.points)):
            line = LineS(self.points[i], self.points[(i+1)%len(self.points)])
            final = min(final, line.tangent_vector(point))
        return final

    def distance_to(self, point):
        return self.tangent_vector(point).norm()


class Constraint:
    def __init__(self, objects, priority=1):
        self.objects = objects

    def apply(self):
        for obj in self.objects:
            pass

class EdgeConstraint(Constraint):
    def __init__(self, objects, priority=0, sensitivity = 0.01):
        super().__init__(objects)
        if len(objects) < 2:
            raise Exception("EdgeConstraint must have at least two objects")
        self.parent_object = objects[0]
        self.child_objects = objects[1:]
        self.sensitivity = sensitivity

    def apply(self):
        for child in self.child_objects:
            host_to_child = child.tangent_vector(self.parent_object.location)
            child_edge = self.parent_object.location + host_to_child
            child_edge_to_parent_edge = self.parent_object.tangent_vector(child_edge)
            if child_edge_to_parent_edge.norm() > self.sensitivity:
                child.location = child.location + child_edge_to_parent_edge


if __name__ == "__main__":
    scene = Scene()
    #make a shape
    shape = PolygonS([V(random.randint(0, 20), random.randint(-20, 20)) for i in range(3)])
    shape2 = CircleS(V(random.randint(-20, -5), random.randint(-20, 20)), 5)

    shape.render_in(scene, Material("#"), fill_material=Material("."))
    shape2.render_in(scene, Material("#"), fill_material=Material("*"))
    print(scene.render())

    #make a constraint
    edge_constraint = EdgeConstraint([shape, shape2], sensitivity=0.1)
    edge_constraint.apply()

    scene = Scene([])
    print(scene.objects)
    shape.render_in(scene, Material("#"), fill_material=Material("."))
    shape2.render_in(scene, Material("#"), fill_material=Material("*"))
    print(scene.render())

    for i in range(100):
        edge_constraint.apply()
        scene = Scene([])
        print(scene.objects)
        shape.render_in(scene, Material("#"), fill_material=Material("."))
        shape2.render_in(scene, Material("#"), fill_material=Material("*"))
        print(scene.render())
        time.sleep(0.1)
