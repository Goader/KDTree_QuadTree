from matplotlib.patches import Rectangle
import numpy as np


class _PointsCollection:
    def __init__(self, points, **kwargs):
        self._points = points
        self._kwargs = kwargs

    @property
    def points(self):
        return np.array(self._points)

    @property
    def kwargs(self):
        return self._kwargs


class _LinesCollection:
    def __init__(self, lines, **kwargs):
        self._lines = lines
        self._kwargs = kwargs

    @property
    def lines(self):
        return np.array(self._lines)

    @property
    def kwargs(self):
        return self._kwargs


class VisualiserContainer:
    def __init__(self):
        self._lines_collections = []
        self._points_collections = []
        self._rects = []

    @property
    def points_collections(self):
        return self._points_collections

    @property
    def lines_collections(self):
        return self._lines_collections

    @property
    def rects(self):
        return self._rects

    def is_empty(self):
        return len(self._lines_collections) == 0 \
           and len(self._points_collections) == 0 \
           and len(self._rects) == 0

    def add_points(self, points, **kwargs):
        coll = _PointsCollection(points, **kwargs)
        self._points_collections.append(coll)

    def add_lines(self, lines, **kwargs):
        coll = _LinesCollection(lines, **kwargs)
        self._lines_collections.append(coll)

    def add_rect(self, rect, **kwargs):
        width = rect.ptp_by_axis(0)
        height = rect.ptp_by_axis(1)
        xy = rect.lowerleft.point
        self._rects.append(Rectangle(xy, width, height, **kwargs))
