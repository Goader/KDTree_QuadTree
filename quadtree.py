from collections import Collection

from geometry.Point import Point
from geometry.Rect import Rect


class _QuadTreeNode:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.right_upper = None
        self.right_upper = None
        self.left_down = None
        self.left_upper = None

    def _subdivide(self):
        lowerleft = self.boundary.lowerleft
        upperright = self.boundary.upperright
        xthreshold = (lowerleft.get_axis(0) + upperright.get_axis(0)) / 2
        ythreshold = (lowerleft.get_axis(1) + upperright.get_axis(1)) / 2

        left, right = self.boundary.divide(0, xthreshold)
        lowerleft_rect, upperleft_rect = left.divide(1, ythreshold)
        lowerright_rect, upperright_rect = right.divide(1, ythreshold)

        self.right_upper = _QuadTreeNode(upperright_rect, self.capacity)
        self.left_upper = _QuadTreeNode(upperleft_rect, self.capacity)
        self.left_down = _QuadTreeNode(lowerright_rect, self.capacity)
        self.right_down = _QuadTreeNode(lowerleft_rect, self.capacity)

    def insert(self, point):
        if not self.boundary.contains_point(point):
            return False
        self.points.append(point)
        if self.capacity < len(self.points):
            if not self.divided:
                self._subdivide()
                self.divided = True
        # the construction using ORs means it tries to insert the point
        # until some subnode returns true as result, that means it has been inserted
                for p in self.points:
                    self.right_upper.insert(p) \
                        or self.right_down.insert(p) \
                        or self.left_upper.insert(p) \
                        or self.left_down.insert(p)
            else:
                self.right_upper.insert(point) \
                    or self.right_down.insert(point) \
                    or self.left_upper.insert(point) \
                    or self.left_down.insert(point)
        return True

    def points_in_rec(self, rect):
        if not rect.overlaps(self.boundary):
            return []
        if rect.contains_rect(self.boundary):
            return self.points
        result = []
        if self.divided:
            result.extend(self.left_down.points_in_rec(rect))
            result.extend(self.left_upper.points_in_rec(rect))
            result.extend(self.right_down.points_in_rec(rect))
            result.extend(self.right_upper.points_in_rec(rect))
        else:
            result.extend([point for point in self.points
                           if rect.contains_point(point)])
        return result


class QuadTree:
    def __init__(self, rect, capacity, points=None):
        if not isinstance(rect, Rect):
            if not isinstance(rect, Collection) \
                    or not len(rect) == 2:
                raise TypeError("Passed argument is not a Rect object or "
                                + "cannot be treated as one")
            rect = Rect(*rect)
        self._node = _QuadTreeNode(rect, capacity)
        if points is not None:
            points = list(map(Point, points))
            self.insert_all(points)

    def insert(self, point):
        self._node.insert(point)

    def insert_all(self, points):
        for point in points:
            self._node.insert(point)

    def find_points_in(self, rect, raw=True):
        result = self._node.points_in_rec(rect)
        return result if not raw else [p.point for p in result]
