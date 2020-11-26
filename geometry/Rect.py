from functools import reduce
from geometry.Point import Point


class Rect:
    def __init__(self, lowerleft, upperright):
        if not isinstance(lowerleft, Point):
            lowerleft = Point(lowerleft)
        if not isinstance(upperright, Point):
            upperright = Point(upperright)
        self._lowerleft = lowerleft
        self._upperright = upperright

    def __eq__(self, other):
        return self.lowerleft == other.lowerleft and self.upperright == other.upperright

    @property
    def lowerleft(self):
        return self._lowerleft

    @property
    def upperright(self):
        return self._upperright

    @classmethod
    def from_points(cls, points):
        upr = reduce(lambda acc, x: acc.find_max(x), points)
        lwl = reduce(lambda acc, x: acc.find_min(x), points)
        return cls(lwl, upr)

    def overlaps(self, rect):
        return self.lowerleft.precedes(rect.upperright) \
               and rect.lowerleft.precedes(self.upperright)

    def contains_rect(self, rect):
        return self.lowerleft.precedes(rect.lowerleft) \
               and self.upperright.follows(rect.upperright)

    def contains_point(self, point):
        if not isinstance(point, Point):
            point = Point(point)
        return self.lowerleft.precedes(point) and self.upperright.follows(point)

    def divide(self, axis, threshold):
        upr = self.upperright
        lwl = self.lowerleft

        if lwl.point[axis] > threshold or upr.point[axis] < threshold:
            raise ValueError("Wrong threshold passed. It does not belong to this rectangular")

        """
         ---------------upr1------upr2
         |               |         |   upr2 == original upperright
         |               |         |
         |               |         |
         |               |         |   lwl1 == original lowerleft
        lwl1------------lwl2--------
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
