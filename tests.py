from kdtree import KDTree
from quadtree import QuadTree
import numpy as np
from geometry.Rect import Rect

"""
This tests print out information.
For the time to be printed, make sure there are active decorators @timeit
above the "__init__" and "find_points_in" methods in both kdtree.py and quadtree.py

@timeit decorator takes 2 arguments: 
    title - less than 26 characters string which will be printed before the time
    precision - integer which specifies how many decimals will be printed
"""


def test_random(count=200, capacity=1):
    points = np.random.uniform(0, 100, (count, 2))
    ktree = KDTree(points)
    qtree = QuadTree(Rect((0, 0), (100, 100)), capacity, points=points, visualise=False)

    rect = Rect((20, 20), (65, 80))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_grid(power=3, capacity=1):
    points = []
    for i in range(1 << power + 1):
        for j in range(1 << power + 1):
            point = (i * 32 / (1 << power), j * 32 / (1 << power))
            points.append(point)
    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (32, 32)), capacity, points=points, visualise=False)

    rect = Rect((2, 3), (16, 40))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_clusters(count=200, capacity=1):
    points = []
    for i in range(count // 4):
        point = (np.random.uniform(0, 20), np.random.uniform(0, 25))
        points.append(point)
    for i in range(count // 4):
        point = (np.random.uniform(40, 60), np.random.uniform(50, 75))
        points.append(point)
    for i in range(count // 4):
        point = (np.random.uniform(0, 20), np.random.uniform(50, 75))
        points.append(point)
    for i in range(count // 4 + count % 4):
        point = (np.random.uniform(60, 80), np.random.uniform(25, 50))
        points.append(point)

    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (80, 100)), capacity, points=points, visualise=False)

    rect = Rect((10, 8), (70, 40))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_clusters2(count=200, capacity=1):
    points = []
    for i in range(count // 4):
        point = (np.random.uniform(0, 20), np.random.uniform(0, 25))
        points.append(point)
    for i in range(count // 4):
        point = (np.random.uniform(40, 60), np.random.uniform(50, 75))
        points.append(point)
    for i in range(count // 4):
        point = (np.random.uniform(0, 20), np.random.uniform(50, 75))
        points.append(point)
    for i in range(count // 4 + count % 4):
        point = (np.random.uniform(60, 80), np.random.uniform(25, 50))
        points.append(point)

    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (80, 100)), capacity, points=points, visualise=False)

    rect = Rect((0, 0), (60, 75))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_outliers(count=200, capacity=1):
    points = []
    for i in range((count * 99) // 100):
        point = (np.random.uniform(40, 50), np.random.uniform(30, 40))
        points.append(point)
    for i in range(count - (count * 99) // 100):
        point = (np.random.uniform(0, 100), np.random.uniform(0, 100))
        points.append(point)

    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (100, 100)), capacity, points=points, visualise=False)

    rect = Rect((45, 23), (83, 28))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_outliers2(count=200, capacity=1):
    assert count >= 4, 'Count must be at least 4'
    points = np.random.uniform(0, 10, (count, 2))
    points[-1] = np.array((1 << 62, 1 << 62))
    points[-2] = np.array((0, 1 << 62))
    points[-3] = np.array((1 << 62, 0))

    ktree = KDTree(points)
    qtree = QuadTree(Rect((0, 0), (1 << 62, 1 << 62)), capacity, points=points)

    rect = Rect((5, 5), (1 << 61 + 1 << 60 + 1 << 59 + 1,
                         1 << 61 + 1 << 60 + 1 << 59 + 1))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_cross(count=200, capacity=1):
    points = []
    for i in range(count // 2):
        point = (np.random.uniform(0, 50), 50)
        points.append(point)
    for i in range(count // 2 + count % 2):
        point = (25, np.random.uniform(0, 100))
        points.append(point)
    points = np.array(points)
    ktree = KDTree(points)
    qtree = QuadTree(Rect((0, 0), (50, 100)), capacity, points=points)

    rect = Rect((20, 20), (40, 60))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_rectangle(count=200, capacity=1):
    points = []
    for i in range(count // 4):
        point = (np.random.uniform(0, 100), 0)
        points.append(point)
    for i in range(count // 4):
        point = (0, np.random.uniform(0, 100))
        points.append(point)
    for i in range(count // 4):
        point = (100, np.random.uniform(0, 100))
        points.append(point)
    for i in range(count // 4 + count % 4):
        point = (np.random.uniform(0, 100), 100)
        points.append(point)
    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (100, 100)), capacity, points=points, visualise=False)

    rect = Rect((-20, 20), (40, 120))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_normal_distribution(count=200, capacity=1):
    points = np.random.normal(50, 10, (count, 2))
    for point in points:
        for axis in range(2):
            if not 0 <= point[axis] <= 100:
                point[axis] = np.random.uniform(0, 100)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (100, 100)), capacity, points=points, visualise=False)

    rect = Rect((20, 20), (65, 80))
    print('-' * 35)
    ktree.find_points_in(rect)
    qtree.find_points_in(rect)


def test_all(count=200, power=3, capacity=1):
    funcs = [test_random, test_outliers, test_outliers2, test_normal_distribution,
             test_clusters, test_clusters2, test_cross, test_rectangle]
    for func in funcs:
        print('-' * 20, func.__name__, '-' * (30 - len(func.__name__)),
              f'parameters - count: {count}, capacity: {capacity}')
        try:
            func(count=count, capacity=capacity)
        except ValueError:
            print(f'ERROR: duplicates found')

    print('-' * 20, test_grid.__name__, '-' * (30 - len(test_grid.__name__)),
          f'parameters - power: {power}, capacity: {capacity}')
    try:
        test_grid(power=power, capacity=capacity)
    except ValueError:
        print(f'ERROR: duplicates found')


if __name__ == '__main__':
    test_all()
