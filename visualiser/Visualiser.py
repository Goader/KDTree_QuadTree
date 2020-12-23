from visualiser.VisualiserContainer import VisualiserContainer
from matplotlib.widgets import Button
from copy import copy
import matplotlib.pyplot as plt


class Visualiser:
    def __init__(self, scope_rect):
        if not scope_rect.dimensions == 2:
            raise ValueError('Visualiser supports only 2D objects (scope_rect)')

        self._scenes = [VisualiserContainer()]
        self._scenes_count = 1

        lwl, upr = scope_rect.lowerleft.point, scope_rect.upperright.point

        self._top_lim = upr[1]
        self._bottom_lim = lwl[1]
        self._left_lim = lwl[0]
        self._right_lim = upr[0]

        self._active_scene = None

    def add_points(self, points, **kwargs):
        self._scenes[-1].add_points(points, **kwargs)

    def add_lines(self, lines, **kwargs):
        self._scenes[-1].add_lines(lines, **kwargs)

    def add_rect(self, rect, **kwargs):
        self._scenes[-1].add_rect(rect, **kwargs)

    def next_scene(self):
        self._scenes_count += 1
        self._scenes.append(VisualiserContainer())

    def _callback_next(self, event):
        self._active_scene = (self._active_scene + 1) % self._scenes_count
        self._draw_scene()

    def _callback_prev(self, event):
        self._active_scene = (self._active_scene - 1) % self._scenes_count
        self._draw_scene()

    def _draw_scene(self):
        plt.close()
        plt.figure(figsize=(12, 8))

        ax_plot = plt.axes((0.05, 0.2, 0.9, 0.7))
        ax_prev = plt.axes((0.2, 0.03, 0.2, 0.09))
        ax_next = plt.axes((0.6, 0.03, 0.2, 0.09))

        btn_prev = Button(ax_prev, 'PREVIOUS', color='darkorange', hovercolor='orange')
        btn_next = Button(ax_next, 'NEXT', color='darkorange', hovercolor='orange')

        btn_prev.on_clicked(self._callback_prev)
        btn_next.on_clicked(self._callback_next)

        ax_plot.set_xlim(left=self._left_lim, right=self._right_lim)
        ax_plot.set_ylim(bottom=self._bottom_lim, top=self._top_lim)

        container = self._scenes[self._active_scene]

        for rect in container.rects:
            ax_plot.add_patch(copy(rect))

        # recheck
        for lcoll in container.lines_collections:
            for line in lcoll.lines:
                ax_plot.plot(line[:, 0], line[:, 1], **lcoll.kwargs, zorder=1)

        for pcoll in container.points_collections:
            ax_plot.scatter(pcoll.points[:, 0], pcoll.points[:, 1], **pcoll.kwargs, zorder=2)

        plt.show()

    def draw(self):
        # remove is_empty() if empty plots can be drawn
        # recheck if buttons behaviour match expected with scenes count equal to 0
        if self._scenes_count == 0 and self._scenes[0].is_empty():
            raise ValueError('Visualiser has nothing to show. Try adding some objects')

        self._active_scene = 0

        self._draw_scene()

        self._active_scene = None

