from visualiser.Visualiser import Visualiser


class SearchVisualiser(Visualiser):
    def __init__(self, scope_rect, builder):
        super().__init__(scope_rect)
        self._original_background = builder.final_scene_container()
        self._background = self._original_background.copy()
        self._scenes[-1] = self._background.copy()

    def clear(self):
        self._background = self._original_background.copy()
        self._scenes_count = 1
        self._scenes = [self._background.copy()]

    def next_scene(self):
        self._scenes_count += 1
        self._scenes.append(self._background.copy())

    def add_background_points(self, points, **kwargs):
        self._background.add_points(points, **kwargs)

    def add_background_lines(self, lines, **kwargs):
        self._background.add_lines(lines, **kwargs)

    def add_background_rect(self, rect, **kwargs):
        self._background.add_rect(rect, **kwargs)
