from geometry.Point import Point
from geometry.Rect import Rect
from collections.abc import Iterable, Sized
import numpy as np


class _KDTreeNode:
    def __init__(self, point=None, points=None):
        self._leaf = point is not None
        self._point = point
        self._points = points
        self._condition = None
        self._condition_axis = None
        self._condition_threshold = None
        self._left = None
        self._right = None
        self._rect = None

    @property
    def condition(self):
        return self._condition

    @property
    def point(self):
        return self._point

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        if not self._leaf and isinstance(left, _KDTreeNode):
            self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        if not self._leaf and isinstance(right, _KDTreeNode):
            self._right = right

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = rect

    def is_leaf(self):
        return self._leaf

    def set_condition(self, axis, threshold):
        self._condition = lambda point: point.get_axis(axis) <= threshold
        self._condition_axis = axis
        self._condition_threshold = threshold

    # maybe should change it to np.array instead of list
    def search_inside_rect(self, rect):
        if self.is_leaf():
            if rect.contains_point(self._point):
                return [self._point]
            else:
                return []
        if not rect.overlaps(self._rect):
            return []
        if rect.contains_rect(self._rect):
            return self._points

        res = []
        res.extend(self._left.search_inside_rect(rect))
        res.extend(self._right.search_inside_rect(rect))
        return res


class KDTree:
    def __init__(self, points, dimensions=2):
        if len(points) == 0:
            raise ValueError("KDTree cannot be instantiated with no points inside")

        self._dimensions = dimensions
        self._points = np.array(list(map(Point, points)), dtype=Point)
        self._full_rect = Rect.from_points(self._points)
        self._root = self._build_tree(self._points, self._full_rect)

    def __contains__(self, point):
        return self.contains(point)

    # points is 2d array (axis x values)
    @staticmethod
    def _get_condition_axis(points):
        ptp = np.ptp(points)
        return np.argmax(ptp)

    # points is 2d array (axis x values)
    @staticmethod
    def _get_condition_threshold(points, axis):
        # think about whether it is okay for median with floats
        return np.median(points[axis])

    # points is a numpy array of Point objects
    def _build_tree(self, points, rect):
        # think whether points can be an empty array
        if len(points) == 1:
            return _KDTreeNode(point=points[0])

        points_by_axes = np.array(
            [[point.get_axis(axis) for point in points]
             for axis in range(self._dimensions)]
        )
        cond_axis = self._get_condition_axis(points_by_axes)
        cond_threshold = self._get_condition_threshold(points_by_axes, cond_axis)

        node = _KDTreeNode(points=points)
        node.set_condition(cond_axis, cond_threshold)
        node.rect = rect

        left_rect, right_rect = rect.divide(cond_axis, cond_threshold)

        left_points = [point for point in points if node.condition(point)]
        right_points = [point for point in points if not node.condition(point)]

        node.left = self._build_tree(left_points, left_rect)
        node.right = self._build_tree(right_points, right_rect)

        return node

    def _contains_recur(self, node, point):
        if node.is_leaf():
            return point == node.point
        if node.condition(point):
            return self._contains_recur(node.left, point)
        else:
            return self._contains_recur(node.right, point)

    def contains(self, point):
        if not isinstance(point, Point):
            if isinstance(point, Iterable) and isinstance(point, Sized):
                if len(point) == self._dimensions:
                    point = Point(point)
                else:
                    raise TypeError("The dimensions of the given point and KDTree do not match")
            else:
                raise TypeError("Passed object is not iterable or Point instance")

        return self._contains_recur(self._root, point)

    # should find a better name for this :)
    def find_points_in(self, rect):
        return self._root.search_inside_rect(rect)
