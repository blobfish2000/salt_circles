import random
from render import *
import math
import time

edge_mats = Material.list_to_mat("0#$@",1)
fill_mat = Material('.',0)
clear_mat = Material(' ',99,99)

#basic polygon rotation test

ngon = 2
rotation = 0
grow = True
speed = 0
radius = 10
while True:
    #pentagon points
    points = []
    for i in range(ngon):
        points.append((radius*math.cos(i*2*math.pi/ngon + rotation),radius*math.sin(i*2*math.pi/ngon + rotation)))


    pentagon = Polygon(points,edge_mats,fill_mat)

    objects = [pentagon]

    scene = Scene(objects)

    print(scene.render())
    
    if grow:
        radius += speed
        speed += 0.1
        if radius >= 20:
            grow = False
            speed = 0
    else:
        radius -= speed
        speed += 0.1
        if radius <= 3:
            grow = True
            speed = 0
            ngon += 1
            if ngon > 8:
                ngon = 2

    rotation += 0.1
    if rotation >= 2*math.pi:
        rotation = 0
    time.sleep(0.1)

