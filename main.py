from kdtree import KDTree
import numpy as np
from geometry.Rect import Rect


if __name__ == '__main__':
    points = [(14, 93), (17, 73), (19, 33),
              (27, 68), (29, 72), (33, 30),
              (50, 57), (59, 17), (62, 63),
              (66, 41), (85, 56), (86, 56),
              (91, 11), (92, 98), (98, 47)]
    points = np.array(points)
    tree = KDTree(points, visualise=True)

    rect = Rect((30, 10), (95, 70))
    print('-' * 50)
    print(list(map(lambda x: x.point, tree.find_points_in(rect))))
