from collections import Collection
from functools import reduce
from geometry.Point import Point
import numpy as np


class Rect:
    def __init__(self, lowerleft, upperright):
        if not isinstance(lowerleft, Point):
            lowerleft = Point(lowerleft)
        if not isinstance(upperright, Point):
            upperright = Point(upperright)
        if lowerleft.axes_count != upperright.axes_count:
            raise TypeError('Point dimensions do not match. It is not possible to instantiate Rect')
        self._dimensions = lowerleft.axes_count
        self._lowerleft = lowerleft
        self._upperright = upperright

    def __eq__(self, other):
        return self.lowerleft == other.lowerleft and self.upperright == other.upperright

    def __str__(self):
        return f'{self._lowerleft} - {self._upperright}'

    def __repr__(self):
        return self.__str__()

    @property
    def lowerleft(self):
        return self._lowerleft

    @property
    def upperright(self):
        return self._upperright

    @property
    def dimensions(self):
        return self._dimensions

    def ptp_by_axis(self, axis):
        return self.upperright.get_axis(axis) - self.lowerleft.get_axis(axis)

    @classmethod
    def from_points(cls, points):
        upr = reduce(lambda acc, x: acc.find_max(x), points)
        lwl = reduce(lambda acc, x: acc.find_min(x), points)
        return cls(lwl, upr)

    def overlaps(self, rect):
        return self.lowerleft.precedes(rect.upperright) \
               and rect.lowerleft.precedes(self.upperright)

    def contains_rect(self, rect):
        if not isinstance(rect, Rect):
            if not isinstance(rect, Collection) \
                    or not len(rect) == 2:
                raise TypeError("Passed argument is not a Rect object or "
                                + "cannot be treated as one")
            rect = Rect(*rect)
        return self.lowerleft.precedes(rect.lowerleft) \
            and self.upperright.follows(rect.upperright)

    def contains_point(self, point):
        if not isinstance(point, Point):
            point = Point(point)
        return self.lowerleft.precedes(point) and self.upperright.follows(point)

    def divide(self, axis, threshold):
        upr = self.upperright
        lwl = self.lowerleft

        if lwl.get_axis(axis) > threshold or upr.get_axis(axis) < threshold:
            raise ValueError("Wrong threshold passed. It does not belong to this rectangular")

        """
         +--------------upr1------upr2
         |               |         |   upr2 == original upperright
         |               |         |
         |               |         |
         |               |         |   lwl1 == original lowerleft
        lwl1------------lwl2-------+
        """

        lwl1 = lwl
        upr2 = upr

        # changing value of particular axis to get upr1 and lwl2
        upr1 = upr.point
        lwl2 = lwl.point
        upr1[axis] = threshold
        lwl2[axis] = threshold

        upr1 = Point(upr1)
        lwl2 = Point(lwl2)

        return Rect(lwl1, upr1), Rect(lwl2, upr2)

    def intersection(self, rect):
        if not self.overlaps(rect):
            return None
        lowerleft = self.lowerleft.find_max(rect.lowerleft)
        upperright = self.upperright.find_min(rect.upperright)

        return Rect(lowerleft, upperright)

    def add_border(self, border_width_ratio, preserve_type=True):
        lowerleft = np.zeros(self._dimensions)
        upperright = np.zeros(self._dimensions)

        for idx, lwl_axis, upr_axis in zip(range(self._dimensions),
                                           self._lowerleft.point,
                                           self._upperright.point):
            if preserve_type:
                value_class = type(self._lowerleft.point[idx])
            else:
                value_class = float
            border_diff = value_class(border_width_ratio * (upr_axis - lwl_axis))
            lowerleft[idx] = lwl_axis - border_diff
            upperright[idx] = upr_axis + border_diff

        return Rect(Point(lowerleft), Point(upperright))
