from kdtree import KDTree
import matplotlib.pyplot as plt
import numpy as np
from geometry import Rect


if __name__ == '__main__':
    points = [(10, 10),
              (21, 32),
              (40, 84),
              (96, 19),
              (44, 33),
              (16, 12),
              (76, 15)]
    points = np.array(points)
    plt.scatter(points[:, 0], points[:, 1])
    # plt.show()
    tree = KDTree(points)
    print(tree.is_elem((76, 15)))
    rect = Rect((10, 10), (21, 85))
    print(list(map(lambda x: x.point, tree.search_inside_rect(rect))))
