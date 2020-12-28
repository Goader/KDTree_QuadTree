from kdtree import KDTree
from quadtree import QuadTree
import numpy as np
from geometry.Rect import Rect
import sys

if __name__ == '__main__':
    points = [(11, 12), (12, 45), (18, 68), (19, 62), (20, 25),
              (23, 17), (23, 68), (24, 51), (25, 98), (28, 73),
              (28, 83), (32, 80), (36, 15), (36, 59), (36, 73),
              (37, 59), (53, 64), (54, 81), (55, 98), (57, 87),
              (64, 28), (71, 53), (73, 54), (75, 77), (83, 70),
              (89, 78), (91, 84), (94, 63), (99, 68), (99, 92)]
    # points = [(11, 10), (12, 10), (18, 10), (19, 10), (20, 10),
    #           (23, 10), (27, 10), (24, 10), (25, 10), (28, 10),
    #           (29, 10), (32, 11), (39, 10), (40, 10), (41, 10),
    #           (37, 10), (53, 10), (54, 10), (55, 10), (57, 10),
    #           (64, 10), (71, 10), (73, 10), (75, 10), (83, 10),
    #           (89, 10), (91, 10), (94, 10), (98, 10), (99, 10)]
    points = np.array(points)
    ktree = KDTree(points)
    qtree = QuadTree(Rect((10, 10), (100, 100)), 1, points=points, visualise=True)

    print(sys.getrecursionlimit())
    sys.setrecursionlimit(10000)

    rect = Rect((22, 10), (95, 83))
    print('-' * 50)
    print(ktree.find_points_in(rect))
    print(qtree.find_points_in(rect))

    for p in map(tuple, ktree.find_points_in(rect)):
        if p not in map(tuple, qtree.find_points_in(rect)):
            print('houston, we have a problem here')
