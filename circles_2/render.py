import random

class PixelBuffer():
    # holds a 2D array of material lists 
    def __init__(self, width, height, background = None):
        self.width = width
        self.height = height
        if background is None:
            background = Material(' ',-1)
        self.buffer = [[[background] for x in range(width)] for y in range(height)]

    def paint_pixel(self, x, y, mat):
        # adds a material to the pixel buffer at the given coordinates
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            if type(mat) is Material:
                self.buffer[y][x].append(mat)
            elif type(mat) is list:
                self.buffer[y][x] += mat
            else:
                raise TypeError('mat must be a Material or a list of Materials')

    def viewport_to_buffer(self, x, y):
        # transforms a point in viewport coordinates (-1,1) to pixel buffer coordinates
        # returns a tuple (x, y) of pixel buffer coordinates
        x = int((x + 1) / 2 * self.width)
        y = int((y + 1) / 2 * self.height)
        return (x, y)

    def render(self, seed = 0):
        s = ''
        random.seed(seed)
        for row in self.buffer:
            for pixel in row:
                max_priority = max([mat.priority for mat in pixel])
                max_priority_mats = [mat for mat in pixel if mat.priority == max_priority]
                sum_mix = sum([mat.mix for mat in max_priority_mats])
                r = random.random() * sum_mix
                for mat in max_priority_mats:
                    r -= mat.mix
                    if r <= 0:
                        s += mat.char
                        s += ' '
                        break
            s += '\n'
        return s

    def __str__(self):
        return self.render()
                

class Viewport():
    # holds the coordinate bounds of a viewport and a pixel buffer
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = x_max - x_min
        self.height = y_max - y_min

    def world_to_viewport(self, x, y):
        # transforms a point in world coordinates to viewport coordinates (-1,1)
        # returns a tuple (x, y) of viewport coordinates
        x = (x - self.x_min) / self.width * 2 - 1
        y = (y - self.y_min) / self.height * 2 - 1
        return (x, y)

class Scene():
    # holds a list of objects to be rendered, the coordinate bounds of a viewport, and a pixel buffer
    # the viewport is a rectangle in the scene that will be rendered to the pixel buffer

    def __init__(self, objects = [], viewport = None, pixel_buffer = None):
        self.objects = objects
        if viewport is None:
            viewport = Viewport(-20, 20, -20, 20)
        self.viewport = viewport
        if pixel_buffer is None:
            pixel_buffer = PixelBuffer(40, 40)
        self.pixel_buffer = pixel_buffer

    def render(self):
        for obj in self.objects:
            obj.render(self)
        return self.pixel_buffer.render()

class Material():
    def list_to_mat(l, priority = 0):
        return [Material(x,priority) for x in l]

    def __init__(self, char, priority = 0, mix = 1):
        self.char = char
        self.priority = priority
        self.mix = mix

class Renderable():
    # an object that can be rendered
    def render(self, scene):
        pass

class Circle(Renderable):
    def __init__(self, x, y, radius, edge_mat, fill_mat = None):
        self.x = x
        self.y = y
        self.radius = radius
        self.edge_mat = edge_mat
        self.fill_mat = fill_mat

    def render(self, scene):
        vp = scene.viewport
        pb = scene.pixel_buffer
        # draw a circle into the pixel buffer
        # transform the circle's center point from world coordinates to viewport coordinates then to pixel buffer coordinates
        x, y = pb.viewport_to_buffer(*vp.world_to_viewport(self.x, self.y))
        # transform the circle's radius from world coordinates to viewport coordinates
        radius = pb.viewport_to_buffer(*vp.world_to_viewport(self.radius, 0))[0] - pb.viewport_to_buffer(0, 0)[0]
        # test if the circle is completely outside the pixel buffer
        if x + radius < 0 or x - radius >= pb.width or y + radius < 0 or y - radius >= pb.height:
            return false
        # use the midpoint circle algorithm to draw the circle
        # https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
        x0 = radius
        y0 = 0
        radius_error = 1 - x0
        while x0 >= y0:
            # draw the circle's 8 octants
            for i in [-1, 1]:
                for j in [-1, 1]:
                    pb.paint_pixel(x + i * x0, y + j * y0, self.edge_mat)
                    pb.paint_pixel(x + i * y0, y + j * x0, self.edge_mat)
            y0 += 1
            if radius_error < 0:
                radius_error += 2 * y0 + 1
            else:
                x0 -= 1
                radius_error += 2 * (y0 - x0 + 1)

        # fill the circle if a fill material was provided
        if self.fill_mat is not None:
            for xp in range(-radius,radius):
                for yp in range(-radius,radius):
                    if xp * xp + yp * yp <= radius * radius:
                        xf = xp + x
                        yf = yp + y
                        pb.paint_pixel(xf, yf, self.fill_mat)
        return True


class Line(Renderable):

    def __init__(self, x1, y1, x2, y2, mat):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mat = mat

    def render(self, scene):
        vp = scene.viewport
        pb = scene.pixel_buffer

        # transform the line's endpoints from world coordinates to viewport coordinates then to pixel buffer coordinates
        x1, y1 = pb.viewport_to_buffer(*vp.world_to_viewport(self.x1, self.y1))
        x2, y2 = pb.viewport_to_buffer(*vp.world_to_viewport(self.x2, self.y2))

        # test if the line is completely outside the pixel buffer
        if x1 < 0 and x2 < 0 or x1 >= pb.width and x2 >= pb.width or y1 < 0 and y2 < 0 or y1 >= pb.height and y2 >= pb.height:
            return False

        dx = abs(x2 - x1)
        sx = 1 if x1 < x2 else -1
        dy = -abs(y2 - y1)
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        #modified bidirectional bresenham's line algorithm
        while True:
            pb.paint_pixel(x1, y1, self.mat)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy


class Triangle(Renderable):

    def __init__(self, x1, y1, x2, y2, x3, y3, edge_mat, fill_mat = None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.edge_mat = edge_mat
        self.fill_mat = fill_mat

    def render(self, scene):
        # transform the triangle's endpoints from world coordinates to viewport coordinates then to pixel buffer coordinates
        vp = scene.viewport
        pb = scene.pixel_buffer

        x1, y1 = pb.viewport_to_buffer(*vp.world_to_viewport(self.x1, self.y1))
        x2, y2 = pb.viewport_to_buffer(*vp.world_to_viewport(self.x2, self.y2))
        x3, y3 = pb.viewport_to_buffer(*vp.world_to_viewport(self.x3, self.y3))

        # test if the triangle is completely outside the pixel buffer
        if x1 < 0 and x2 < 0 and x3 < 0 or x1 >= pb.width and x2 >= pb.width and x3 >= pb.width or y1 < 0 and y2 < 0 and y3 < 0 or y1 >= pb.height and y2 >= pb.height and y3 >= pb.height:
            return False

        # use the baricentric algorithm to draw the triangle
        # https://en.wikipedia.org/wiki/Barycentric_coordinate_system

        # compute the bounding box of the triangle
        x_min = min(x1, x2, x3)
        x_max = max(x1, x2, x3)
        y_min = min(y1, y2, y3)
        y_max = max(y1, y2, y3)

        # subfunction to test if a point is inside the triangle
        def inside(x, y):
            # compute the barycentric coordinates of the point
            # but first test if the triangle is degenerate
            area = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if area == 0:
                return False
            alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / area
            beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / area
            gamma = 1 - alpha - beta
            # test if the point is inside the triangle
            return alpha >= 0 and beta >= 0 and gamma >= 0


        # draw the edges of the triangle as lines (using world coordinates)
        Line(self.x1, self.y1, self.x2, self.y2, self.edge_mat).render(scene)
        Line(self.x2, self.y2, self.x3, self.y3, self.edge_mat).render(scene)
        Line(self.x3, self.y3, self.x1, self.y1, self.edge_mat).render(scene)

        # fill the triangle if a fill material was provided
        if self.fill_mat is not None:
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    if inside(x, y):
                        pb.paint_pixel(x, y, self.fill_mat)
        return True

class Polygon(Renderable):

    def __init__(self, points, edge_mat, fill_mat = None):
        self.points = points
        self.edge_mat = edge_mat
        self.fill_mat = fill_mat

    def render(self, scene):

        vp = scene.viewport
        pb = scene.pixel_buffer

        # transform the polygon's points from world coordinates to viewport coordinates then to pixel buffer coordinates
        world_coords = self.points
        points = [pb.viewport_to_buffer(*vp.world_to_viewport(x, y)) for x, y in self.points]

        # test if the polygon is completely outside the pixel buffer
        if all(x < 0 for x, y in points) or all(x >= pb.width for x, y in points) or all(y < 0 for x, y in points) or all(y >= pb.height for x, y in points):
            return False

        #break the polygon into triangles (using world coordinates)
        triangles = []
        for i in range(1, len(points) - 1):
            triangles.append((world_coords[0], world_coords[i], world_coords[i + 1]))

        # draw the edges of the polygon as lines (using world coordinates)
        for i in range(len(points)):
            Line(self.points[i][0], self.points[i][1], self.points[(i + 1) % len(points)][0], self.points[(i + 1) % len(points)][1], self.edge_mat).render(scene)

        # fill the polygon if a fill material was provided
        if self.fill_mat is not None:
            for t in triangles:
                Triangle(t[0][0], t[0][1], t[1][0], t[1][1], t[2][0], t[2][1], [], self.fill_mat).render(scene)

