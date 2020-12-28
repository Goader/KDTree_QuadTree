from visualiser.Visualiser import Visualiser


class BuildVisualiser(Visualiser):
    def __init__(self, scope_rect):
        super().__init__(scope_rect)
        self._default_lines = []
        self._default_lines_kwargs = dict()
        self._default_points = []
        self._default_points_kwargs = dict()

    def add_lines(self, lines, **kwargs):
        self._default_lines.extend(lines)
        super().add_lines(lines, **kwargs)

    def next_scene(self):
        super().next_scene()
        self.add_points(self._default_points.copy(), **self._default_points_kwargs)
        super().add_lines(self._default_lines.copy(), **self._default_lines_kwargs)

    def set_lines_kwargs(self, **kwargs):
        self._default_lines_kwargs = kwargs
        return self

    def set_points_kwargs(self, **kwargs):
        self._default_points_kwargs = kwargs
        return self

    def set_points(self, points):
        self._default_points = points
        self.add_points(points, **self._default_points_kwargs)
        return self

    def add_default_points(self, points):
        self._default_points.extend(points)
        return self

    def final_scene_container(self):
        return self._scenes[-1].copy()
