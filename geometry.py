from functools import reduce


class Point:
    def __init__(self, point):
        self._point = point  # could be used numpy array to keep
        self._axes_count = len(self._point)

    # needs refactoring for using multiple dimensions
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def axes_count(self):
        return self._axes_count

    @property
    def point(self):  # can return tuple(point), where point is np.array
        return tuple(self._point)

    # needs refactoring for using multiple dimensions
    @property
    def x(self):
        return self._point[0]

    # needs refactoring for using multiple dimensions
    @property
    def y(self):
        return self._point[1]

    def get_axis(self, axis):
        return self._point[axis]

    # needs refactoring for using multiple dimensions
    def follows(self, other):
        return self.x >= other.x and self.y >= other.y

    # needs refactoring for using multiple dimensions
    def precedes(self, other):
        return self.x <= other.x and self.y <= other.y

    # needs refactoring for using multiple dimensions
    def find_min(self, other):
        return Point((min(self.x, other.x), min(self.y, other.y)))

    # needs refactoring for using multiple dimensions
    def find_max(self, other):
        return Point((max(self.x, other.x), max(self.y, other.y)))


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
        upr = reduce(lambda x, y: x.find_max(y), points)
        lwl = reduce(lambda x, y: x.find_min(y), points)
        return cls(lwl, upr)

    # not sure if works ok for crosses-like rects // seems okay
    def overlaps(self, rect):
        return self.lowerleft.precedes(rect.upperright) \
               and rect.lowerleft.precedes(self.upperright)

    def contains_rect(self, rect):
        return self.lowerleft.precedes(rect.lowerleft) and self.upperright.follows(rect.upperright)

    def contains_point(self, point):
        if not isinstance(point, Point):
            point = Point(point)
        return self.lowerleft.precedes(point) and self.upperright.follows(point)

    def divide(self, axis, threshold):
        upr = self.upperright
        lwl = self.lowerleft

        if lwl.point[axis] > threshold or upr.point[axis] < threshold:
            raise ValueError("Wrong threshold passed. It does not belong to this rectangular")

        lwl1 = lwl
        upr2 = upr
        point_upr1 = list(upr.point)
        point_lwl2 = list(lwl.point)
        point_upr1[axis] = threshold
        point_lwl2[axis] = threshold
        upr1 = Point(point_upr1)
        lwl2 = Point(point_lwl2)

        return Rect(lwl1, upr1), Rect(lwl2, upr2)

    # not sure if is okay // seems to be ok
    def intersection(self, rect):
        if not self.overlaps(rect):
            return None
        lowerleft = self.lowerleft.find_max(rect.lowerleft)
        upperright = self.upperright.find_min(rect.upperright)

        return Rect(lowerleft, upperright)
