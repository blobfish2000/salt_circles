import random

class Node:
    def __init__(self, x, y, children=[]):
        self.x = x
        self.y = y
        self.children = children
