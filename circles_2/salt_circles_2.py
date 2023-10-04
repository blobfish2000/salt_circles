import random
from render import *
import math

edge_mats = Material.list_to_mat("0#$@",1)
fill_mat = Material('.',0)
fill2_mat = Material(' ',0.1)

circle = Circle(0, 0, 10, edge_mats, fill_mat)
circle2 = Circle(0, 0, 5, [], fill2_mat)

objects = [circle, circle2] #[circle, circle2]

#simple star
radius = 9
prev_x = 0
prev_y = 10
for i in range(1,6):
    angle = i * math.pi * 4 / 5
    x = radius * math.sin(angle)
    y = radius * math.cos(angle)
    objects.append(Line(prev_x, prev_y, x, y, edge_mats))
    prev_x = x
    prev_y = y

scene = Scene(objects)

print(scene.render())

