from collections import Collection
import numpy as np

from geometry.Point import Point
from geometry.Rect import Rect
from visualiser.BuildVisualiser import BuildVisualiser
from visualiser.SearchVisualiser import SearchVisualiser
from utils import timeit


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

    def _subdivide(self, visualiser=None):
        lowerleft = self.boundary.lowerleft
        upperright = self.boundary.upperright
        xthreshold = (lowerleft.get_axis(0) + upperright.get_axis(0)) / 2
        ythreshold = (lowerleft.get_axis(1) + upperright.get_axis(1)) / 2

        left, right = self.boundary.divide(0, xthreshold)
        lowerleft_rect, upperleft_rect = left.divide(1, ythreshold)
        lowerright_rect, upperright_rect = right.divide(1, ythreshold)

        if visualiser is not None:
            visualiser.next_scene()
            visualiser.add_lines([(left.upperright.point,
                                   right.lowerleft.point)],
                                 color='darkorange', linewidth=2)
            visualiser.add_lines([(upperleft_rect.lowerleft.point,
                                   lowerright_rect.upperright.point)],
                                 color='darkorange', linewidth=2)

        self.right_upper = _QuadTreeNode(upperright_rect, self.capacity)
        self.left_upper = _QuadTreeNode(upperleft_rect, self.capacity)
        self.left_down = _QuadTreeNode(lowerleft_rect, self.capacity)
        self.right_down = _QuadTreeNode(lowerright_rect, self.capacity)

    def insert(self, point, visualiser=None):
        def visualise(rectangular, color=None):
            if visualiser is not None:
                visualiser.next_scene()
                if color is None:
                    color = 'silver'
                visualiser.add_rect(rectangular, alpha=0.4, color=color)
                visualiser.add_points([point.point], color='midnightblue')

        visualise(self.boundary)
        if not self.boundary.contains_point(point):
            visualise(self.boundary, color='red')
            return False
        visualise(self.boundary, color='lawngreen')
        self.points.append(point)
        if self.capacity < len(self.points):
            if not self.divided:
                visualise(self.boundary, 'yellow')
                self._subdivide(visualiser=visualiser)
                self.divided = True
                # the construction using ORs means that it tries to insert the point
                # until some subnode returns true as result, that means it has been inserted
                for p in self.points:
                    self.right_upper.insert(p, visualiser=visualiser) \
                        or self.right_down.insert(p, visualiser=visualiser) \
                        or self.left_down.insert(p, visualiser=visualiser) \
                        or self.left_upper.insert(p, visualiser=visualiser)
            else:
                self.right_upper.insert(point, visualiser=visualiser) \
                    or self.right_down.insert(point, visualiser=visualiser) \
                    or self.left_down.insert(point, visualiser=visualiser) \
                    or self.left_upper.insert(point, visualiser=visualiser)
        return True

    def points_in_rec(self, rect, visualiser=None):
        def visualise(rectangular, points=None, color=None):
            if visualiser is not None:
                if points is not None and points:
                    points = list(map(lambda x: x.point, points))
                    visualiser.add_background_points(points, color='white', s=7)
                visualiser.next_scene()
                if color is None:
                    color = 'silver'
                visualiser.add_rect(rectangular, alpha=0.4, color=color)

        visualise(self.boundary)
        if not rect.overlaps(self.boundary):
            visualise(self.boundary, color='red')
            return []
        if rect.contains_rect(self.boundary):
            color = 'lawngreen' if self.points else 'red'
            visualise(self.boundary, color=color, points=self.points)
            return self.points
        result = []
        if self.divided:
            result.extend(self.left_down.points_in_rec(rect, visualiser=visualiser))
            result.extend(self.left_upper.points_in_rec(rect, visualiser=visualiser))
            result.extend(self.right_down.points_in_rec(rect, visualiser=visualiser))
            result.extend(self.right_upper.points_in_rec(rect, visualiser=visualiser))
        else:
            found_points = [point for point in self.points
                            if rect.contains_point(point)]
            color = 'lawngreen' if found_points else 'red'
            visualise(self.boundary, color=color, points=found_points)
            result.extend(found_points)
        return result


class QuadTree:
    @timeit('QuadTree construction', 5)
    def __init__(self, rect, capacity, points=None, visualise=False):
        assert capacity > 0, 'Capacity must be a positive integer'
        if not isinstance(rect, Rect):
            if not isinstance(rect, Collection) \
                    or not len(rect) == 2:
                raise TypeError("Passed argument is not a Rect object or "
                                + "cannot be treated as one")
            rect = Rect(*rect)
        self._scope = rect
        self._node = _QuadTreeNode(rect, capacity)
        self._builder = None
        self._searcher = None
        if visualise:
            self._builder = BuildVisualiser(rect.add_border(0.1, preserve_type=False)) \
                .set_lines_kwargs(color='magenta', linewidth=2) \
                .set_points_kwargs(color='green')
            self._searcher = SearchVisualiser(
                rect.add_border(0.1, preserve_type=False),
                self._builder.final_scene_container()
            )
        if points is not None and len(points) > 0:
            points = np.array(points)
            self.insert_all(points)

    def _inserted_visualise(self):
        if self._builder is not None:
            self._builder.next_scene()
            self._builder.draw()
            self._searcher.clear(self._builder.final_scene_container())
            self._builder.clear()

    def _insert(self, point):
        if point.axes_count != 2:
            raise TypeError(f'The dimensions of the point {point} and QuadTree'
                            + ' do not match. Point must have 2 dimensions')
        if not self._scope.contains_point(point):
            raise ValueError(f'The point {point} is not within the initial scope rectangle')
        if self._builder is not None:
            self._builder.add_default_points([point.point])
        # point must not be already in the list!
        for other in self._node.points:
            if point == other:
                raise ValueError('QuadTree cannot handle duplicate points')
        self._node.insert(point, visualiser=self._builder)

    def insert(self, point):
        point = Point(point)
        self._insert(point)
        self._inserted_visualise()

    def insert_all(self, points):
        points = list(map(Point, points))
        for point in points:
            self._insert(point)
        self._inserted_visualise()

    @timeit('QuadTree search', 5)
    def find_points_in(self, rect, raw=True):
        if rect.dimensions != 2:
            raise TypeError("The dimensions of the given Rect object "
                            + "and QuadTree do not match")
        if self._searcher is not None:
            self._searcher.add_background_rect(rect, alpha=0.4,
                                               color='midnightblue')
            self._searcher.next_scene()
        result = self._node.points_in_rec(rect, visualiser=self._searcher)
        if self._searcher is not None:
            self._searcher.next_scene()
            self._searcher.draw()
            self._searcher.clear()
        return result if not raw else [p.point for p in result]
