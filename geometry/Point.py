import numpy as np


class Point:
    def __init__(self, point):
        self._point = np.array(point)
        self._axes_count = len(self._point)

    def __eq__(self, other):
        return np.array_equal(self.point, other.point)

    def __str__(self):
        return str(self._point)

    def __repr__(self):
        return self.__str__()

    @property
    def axes_count(self):
        return self._axes_count

    @property
    def point(self):
        return self._point.copy()

    @property
    def x(self):  # convenient usage for QuadTree implementation
        return self._point[0]

    @property
    def y(self):  # convenient usage for QuadTree implementation
        return self._point[1]

    def get_axis(self, axis):
        return self._point[axis]

    def follows(self, other):
        return np.all(self.point >= other.point)

    def precedes(self, other):
        return np.all(self.point <= other.point)

    def find_min(self, other):
        return Point(np.minimum(self.point, other.point))

    def find_max(self, other):
        return Point(np.maximum(self.point, other.point))
