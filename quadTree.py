

class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

    def follows(self, other):
        return (self.x >= other.x and self.y >= other.y)

    def precedes(self, other):
        return (self.x <= other.x and self.y <= other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()


class Rectangle:
    def __init__(self, left_down_corner, right_upper_corner):
        self.x_down = left_down_corner[0]
        self.y_down = left_down_corner[1]
        self.x_upper = right_upper_corner[0]
        self.y_upper = right_upper_corner[1]

    def intersection_all(self, other):
        return (Point([self.x_down, self.y_down]).precedes(Point([other.x_down, other.y_down])) and
                Point([self.x_upper, self.y_upper]).follows(Point([other.x_upper, other.y_upper])))

    def intersection(self, other):
        return (((Point([self.x_down, self.y_down]).precedes(Point([other.x_down, other.y_down])) and
                  Point([self.x_upper, self.y_upper]).follows(Point([other.x_down, other.y_down]))) or
                 (Point([self.x_down, self.y_down]).precedes(Point([other.x_upper, other.x_upper])) and
                  Point([self.x_upper, self.y_upper]).follows(Point([other.x_upper, other.x_upper])))) or

                ((Point([other.x_down, other.y_down]).precedes(Point([self.x_down, self.y_down])) and
                  Point([other.x_upper, other.y_upper]).follows(Point([self.x_down, self.y_down]))) or
                 (Point([other.x_down, other.y_down]).precedes(Point([self.x_upper, self.x_upper])) and
                  Point([other.x_upper, other.y_upper]).follows(Point([self.x_upper, self.x_upper])))))

    def contains(self, point):
        return (point.x >= self.x_down and point.x <= self.x_upper and point.y >= self.y_down and point.y <= self.y_upper)


class Node:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x_down = self.boundary.x_down
        y_down = self.boundary.y_down
        height = self.boundary.y_upper - self.boundary.y_down
        width = self.boundary.x_upper - self.boundary.x_down
        epsilon = 0.0000001
        right_upper_rectangle = Rectangle([x_down + width / 2 + epsilon, y_down + height / 2],
                                          [x_down + width, y_down + height])
        left_upper_rectangle = Rectangle([x_down, y_down + height / 2], [x_down + width / 2, y_down + height])
        right_down_rectangle = Rectangle([x_down + width / 2 + epsilon, y_down],
                                         [x_down + width, y_down + height / 2 - epsilon])
        left_down_rectangle = Rectangle([x_down, y_down], [x_down + width / 2, y_down + height / 2 - epsilon])
        self.right_upper = Node(right_upper_rectangle, self.capacity)
        self.left_upper = Node(left_upper_rectangle, self.capacity)
        self.left_down = Node(left_down_rectangle, self.capacity)
        self.right_down = Node(right_down_rectangle, self.capacity)

    def insert(self, point):
        if not (self.boundary.contains(point)):
            return
        if (len(self.points) < self.capacity):
            self.points.append(point)
        else:
            if (self.divided == False):
                self.subdivide()
                self.divided = True
                for p in self.points:
                    self.right_upper.insert(p)
                    self.right_down.insert(p)
                    self.left_upper.insert(p)
                    self.left_down.insert(p)
            self.right_upper.insert(point)
            self.right_down.insert(point)
            self.left_upper.insert(point)
            self.left_down.insert(point)
            self.points.append(point)

    def points_in_rec(self, rect, points_to_find):
        if not (rect.intersection(self.boundary)):
            return
        else:
            if (rect.intersection_all(self.boundary)):
                return self.points

            else:
                if (self.divided):
                    self.left_down.points_in_rec(rect, points_to_find)
                    self.left_upper.points_in_rec(rect, points_to_find)
                    self.right_down.points_in_rec(rect, points_to_find)
                    self.right_upper.points_in_rec(rect, points_to_find)

                for p in self.points:
                    if rect.contains(p):
                        points_to_find.append(p)
                return points_to_find


class Quadtree:
    def __init__(self, node):
        self.node = node

    def insert_all(self, points):
        for i in range(len(points)):
            self.node.insert(points[i])

    def find_points_in_rec(self, rectangle):
        points = []
        return self.node.points_in_rec(rectangle, points)


def create_rectangular(points):
    right_upper_corner = Point([float('inf'), float('inf')])
    left_down_corner = Point([float('-inf'), float('-inf')])
    for i in range(len(points)):
        if (points[i].precedes(right_upper_corner)):
            right_upper_corner = points[i]
        if (points[i].follows(left_down_corner)):
            left_down_corner = points[i]
    left_down_corner = [left_down_corner.x, left_down_corner.y]
    right_upper_corner = [right_upper_corner.x, right_upper_corner.y]
    return Rectangle(left_down_corner, right_upper_corner)


rectangular = Rectangle([0, 0], [8, 8])
rectangular1 = Rectangle([3, 4], [8, 8])
node = Node(rectangular, 1)
quadtree = Quadtree(node)
quadtree.insert_all([Point([0, 0]), Point([3, 0]), Point([5, 5]), Point([3, 2]), ])
print(quadtree.find_points_in_rec(rectangular1))
