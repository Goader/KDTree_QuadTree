from geometry.Point import Point
from geometry.Rect import Rect
from visualiser.BuildVisualiser import BuildVisualiser
from visualiser.SearchVisualiser import SearchVisualiser
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

    @property
    def condition_axis(self):
        return self._condition_axis

    @property
    def condition_threshold(self):
        return self._condition_threshold

    def set_condition(self, axis, threshold):
        self._condition = lambda point: point.get_axis(axis) <= threshold
        self._condition_axis = axis
        self._condition_threshold = threshold

    # maybe should change it to np.array instead of list
    def search_inside_rect(self, rect, visualiser=None):
        def visualise(rectangular, points=None, color=None, show_line=False):
            if visualiser is not None:
                if points is not None:
                    points = list(map(lambda x: x.point, points))
                    visualiser.add_background_points(points, color='white', s=7)
                visualiser.next_scene()
                if color is None:
                    color = 'lawngreen' if points is not None else 'red'
                visualiser.add_rect(rectangular, alpha=0.4, color=color)
                if show_line:
                    left_rect, right_rect = self._rect.divide(self._condition_axis,
                                                              self._condition_threshold)
                    visualiser.add_lines([(left_rect.upperright.point,
                                           right_rect.lowerleft.point)],
                                         color='darkorange', linewidth=2)

        if self.is_leaf():
            if rect.contains_point(self._point):
                visualise(self._rect, points=[self._point])
                return [self._point]
            else:
                visualise(self._rect)
                return []
        if not rect.overlaps(self._rect):
            visualise(self._rect)
            return []
        if rect.contains_rect(self._rect):
            visualise(self._rect, self._points)
            return self._points

        res = []
        visualise(self._left.rect, color='silver', show_line=True)
        res.extend(self._left.search_inside_rect(rect, visualiser=visualiser))
        visualise(self._right.rect, color='silver', show_line=True)
        res.extend(self._right.search_inside_rect(rect, visualiser=visualiser))
        return res


class KDTree:
    def __init__(self, points, dimensions=2, visualise=False):
        if len(points) == 0:
            raise ValueError('KDTree cannot be instantiated with no points inside')

        self._dimensions = dimensions
        self._visualise = visualise
        self._points = np.array(list(map(Point, points)), dtype=Point)
        # this KDTree cannot handle points duplicates,
        # still it can be done by storing in Point object the count of points
        for i, point in enumerate(self._points):
            for other in self._points[i+1:]:
                if point == other:
                    raise ValueError('KDTree cannot handle duplicate points')
        self._full_rect = Rect.from_points(self._points)
        self._search_visualiser = None

        builder = None
        if visualise:
            builder = BuildVisualiser(
                self._full_rect.add_border(0.1, preserve_type=False)
            ) \
                .set_points_kwargs(color='green') \
                .set_lines_kwargs(color='magenta', linewidth=2) \
                .set_points(points)
        self._root = self._build_tree(self._points, self._full_rect, visualiser=builder)
        if visualise:
            builder.next_scene()
            builder.draw()
            self._search_visualiser = SearchVisualiser(
                self._full_rect.add_border(0.1, preserve_type=False),
                builder.final_scene_container()
            )

    def __contains__(self, point):
        return self.contains(point)

    # points is 2d array (axis x values)
    @staticmethod
    def _get_condition_axis(points):
        ptp = np.ptp(points, axis=1)
        return np.argmax(ptp)

    # points is 2d array (axis x values)
    @staticmethod
    def _get_condition_threshold(points, axis):
        # think about whether it is okay for median with floats
        return np.median(points[axis])

    # points is a numpy array of Point objects
    def _build_tree(self, points, rect, visualiser=None):
        if visualiser is not None:
            visualiser.next_scene()
            visualiser.add_rect(rect, alpha=0.4, color='silver')
            visualiser.add_points(list(map(lambda x: x.point, points)),
                                  color='midnightblue')

        # think whether points can be an empty array
        if len(points) == 1:
            node = _KDTreeNode(point=points[0])
            node.rect = rect
            return node

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

        if visualiser is not None:
            visualiser.next_scene()
            visualiser.add_rect(rect, alpha=0.4, color='silver')
            visualiser.add_lines([(left_rect.upperright.point,
                                   right_rect.lowerleft.point)],
                                 color='darkorange', linewidth=2)

        left_points = [point for point in points if node.condition(point)]
        right_points = [point for point in points if not node.condition(point)]

        node.left = self._build_tree(left_points, left_rect, visualiser=visualiser)
        node.right = self._build_tree(right_points, right_rect, visualiser=visualiser)

        return node

    def _contains_recur(self, node, point, visualise=True):
        if self._search_visualiser is not None and visualise:
            self._search_visualiser.next_scene()
            if not node.is_leaf():
                left_rect, right_rect = node.rect.divide(node.condition_axis,
                                                         node.condition_threshold)
                self._search_visualiser.add_lines([(left_rect.upperright.point,
                                                    right_rect.lowerleft.point)],
                                                  color='darkorange', linewidth=2)
            self._search_visualiser.add_rect(node.rect, alpha=0.4, color='silver')
        if node.is_leaf():
            if self._search_visualiser is not None and visualise:
                self._search_visualiser.next_scene()
                if point == node.point:
                    self._search_visualiser.add_rect(node.rect, alpha=0.4,
                                                     color='lawngreen')
                else:
                    self._search_visualiser.add_rect(node.rect, alpha=0.4,
                                                     color='red')
            return point == node.point
        if node.condition(point):
            return self._contains_recur(node.left, point, visualise=visualise)
        else:
            return self._contains_recur(node.right, point, visualise=visualise)

    def contains(self, point, visualise=True):
        if not isinstance(point, Point):
            if isinstance(point, Iterable) and isinstance(point, Sized):
                if len(point) == self._dimensions:
                    point = Point(point)
                else:
                    raise TypeError("The dimensions of the given point " \
                                    + "and KDTree do not match")
            else:
                raise TypeError("Passed object is not iterable or Point instance")

        if self._search_visualiser is not None and visualise:
            # if there exists such a point, it will be shown being empty inside
            if self._contains_recur(self._root, point, visualise=False):
                self._search_visualiser.add_background_points([point.point],
                                                              color='white', s=7)
            # and if not, then it will be a typical midnightblue point
            else:
                self._search_visualiser.add_background_points([point.point],
                                                              color='midnightblue')
            self._search_visualiser.next_scene()
        result = self._contains_recur(self._root, point, visualise=visualise)
        if self._search_visualiser is not None and visualise:
            self._search_visualiser.next_scene()
            self._search_visualiser.draw()
            self._search_visualiser.clear()
        return result

    # should find a better name for this :)
    def find_points_in(self, rect, raw=True):
        if self._search_visualiser is not None:
            self._search_visualiser.add_background_rect(rect, alpha=0.4,
                                                        color='midnightblue')
            self._search_visualiser.next_scene()
        result = self._root.search_inside_rect(rect, visualiser=self._search_visualiser)
        if self._search_visualiser is not None:
            self._search_visualiser.next_scene()
            self._search_visualiser.draw()
            self._search_visualiser.clear()
        return result if not raw else [p.point for p in result]
