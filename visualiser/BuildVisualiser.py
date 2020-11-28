from visualiser.Visualiser import Visualiser
from visualiser.VisualiserContainer import VisualiserContainer


class BuildVisualiser(Visualiser):
    def __init__(self, scope_rect):
        super().__init__(scope_rect)

    def final_scene_container(self):
        return self._scenes[self._scenes_count - 1]
