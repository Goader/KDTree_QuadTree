from geometry import Point, Rect
import numpy as np


class KDTreeNode:
    def __init__(self, point=None, points=None):
        self._leaf = point is not None
        self._point = point
        self._points = points
        self._condition = None
        self._condition_axis = None
        self._left = None
        self._right = None
        self._rect = None
        self._condition_threshold = None

    @property
    def condition(self):
        return self._condition

    @property
    def point(self):
        return self._point

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, left):
        if not self._leaf and isinstance(left, KDTreeNode):
            self._left = left

    @right.setter
    def right(self, right):
        if not self._leaf and isinstance(right, KDTreeNode):
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
    def __init__(self, points, dimension=2):
        self.dimension = dimension
        self._points = np.array(list(map(Point, points)), dtype=Point)
        self._full_rect = Rect.from_points(self._points)
        self.root = self.build_tree(self._points, self._full_rect)

    # points is 2d array (axis x values)
    @staticmethod
    def get_condition_axis(points):
        ptp = np.ptp(points)
        return np.argmax(ptp)

    # points is 2d array (axis x values)
    @staticmethod
    def get_condition_threshold(points, axis):
        # think about whether it is okay for median with floats
        return np.median(points[axis])

    # points is a numpy array of Point objects
    def build_tree(self, points, rect):
        # think whether points can be an empty array
        if len(points) == 1:
            return KDTreeNode(point=points[0])

        points_by_axes = np.array(
            [[point.get_axis(axis) for point in points]
             for axis in range(self.dimension)]
        )
        cond_axis = self.get_condition_axis(points_by_axes)
        cond_threshold = self.get_condition_threshold(points_by_axes, cond_axis)

        node = KDTreeNode(points=points)
        node.set_condition(cond_axis, cond_threshold)
        node.rect = rect

        left_rect, right_rect = rect.divide(cond_axis, cond_threshold)

        left_points = [point for point in points if node.condition(point)]
        right_points = [point for point in points if not node.condition(point)]

        node.left = self.build_tree(left_points, left_rect)
        node.right = self.build_tree(right_points, right_rect)

        return node

    def is_elem_aux(self, node, point):
        if node.is_leaf():
            return point == node.point
        if node.condition(point):
            return self.is_elem_aux(node.left, point)
        else:
            return self.is_elem_aux(node.right, point)

    # tmp method to check whether it works ok at this moment
    def is_elem(self, point):
        point = Point(point)
        return self.is_elem_aux(self.root, point)

    def search_inside_rect(self, rect):
        return self.root.search_inside_rect(rect)
