from kdtree import KDTree
import matplotlib.pyplot as plt
import numpy as np
from geometry.Rect import Rect
from visualiser.Visualiser import Visualiser


if __name__ == '__main__':
    points = [(10, 10),
              (21, 32),
              (40, 84),
              (96, 19),
              (44, 33),
              (16, 12),
              (76, 15)]
    points = np.array(points)
    tree = KDTree(points, visualise=True)
    print(tree.contains((76, 15)))
    print((40, 84) in tree)
    print(np.array([44, 33]) in tree)
    tree.contains((40, 56))
    rect = Rect((10, 10), (21, 85))
    print(list(map(lambda x: x.point, tree.find_points_in(rect))))

    # rect = Rect((0,0), (10, 10))
    # rect1 = Rect((4,4), (7, 5))
    # visual = Visualiser(rect)
    # visual.add_points([(3, 4), (5, 4), (7, 8), (5, 5)], color='green')
    # visual.add_lines([[(1, 1), (4, 8)]], color='darkorchid', linewidth=2)
    # visual.add_rect(rect1, alpha=0.6, color='darkorange')
    # visual.draw()
