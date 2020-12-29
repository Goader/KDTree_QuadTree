from kdtree import KDTree
from quadtree import QuadTree
import numpy as np
from geometry.Rect import Rect

def test1():
    points = []
    for i in range(1000):
        point = (np.random.random() *100,np.random.random()*100)
        points.append(point)
    points = np.array(points)
    ktree = KDTree(points)
    qtree = QuadTree(Rect((0, 0), (100, 100)), 1, points=points,visualise=True )

    rect = Rect((20, 20), (65, 80))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))
def test2():
    points = []
    for i in range(33):
        for j in range (33):
            point = (i,j)
            points.append(point)
    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (32, 32)), 1, points=points, visualise=False )

    rect = Rect((2, 3), (16, 40))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))

def test3_A():
    points = []
    for i in range(250):
        point = (np.random.random() * 20, np.random.random() * 25)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20+40, np.random.random() * 25+50)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20, np.random.random() * 25+50)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20+60, np.random.random() * 25+25)
        points.append(point)

    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (80, 100)), 1, points=points, visualise=False )

    rect = Rect((10, 8), (70, 40))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))

def test3_B():
    points = []
    for i in range(250):
        point = (np.random.random() * 20, np.random.random() * 25)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20+40, np.random.random() * 25+50)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20, np.random.random() * 25+50)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 20+60, np.random.random() * 25+25)
        points.append(point)

    points = np.array(points)
    ktree = KDTree(points, visualise=False)
    qtree = QuadTree(Rect((0, 0), (80, 100)), 1, points=points, visualise=False )

    rect = Rect((0, 0), (60, 75))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))

def test4():
        points = []
        for i in range(990):
            point = (np.random.random() * 10+40, np.random.random() * 10+30)
            points.append(point)
        for i in range (10):
            point = (np.random.random() * 100, np.random.random() * 100)
            points.append(point)

        points = np.array(points)
        ktree = KDTree(points, visualise=False)
        qtree = QuadTree(Rect((0, 0), (100, 100)), 1, points=points, visualise=False)

        rect = Rect((45, 23), (83, 28))
        print('-' * 50)
        (ktree.find_points_in(rect))
        (qtree.find_points_in(rect))

def test5():
    points = []
    for i in range(500):
        point = (np.random.random() * 50, 50)
        points.append(point)
    for i in range(500):
        point = (25, np.random.random() * 100)
        points.append(point)
    points = np.array(points)
    ktree = KDTree(points)
    qtree = QuadTree(Rect((0, 0), (50, 100)), 1, points=points)

    rect = Rect((20, 20), (40, 60))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))
def test6():
    points = []
    for i in range(250):
        point = (np.random.random() * 100, 0)
        points.append(point)
    for i in range(250):
        point = (0, np.random.random() * 100)
        points.append(point)
    for i in range(250):
        point = (100, np.random.random() * 100)
        points.append(point)
    for i in range(250):
        point = (np.random.random() * 100, 100)
        points.append(point)
    points = np.array(points)
    ktree = KDTree(points,visualise=True)
    qtree = QuadTree(Rect((0, 0), (100, 100)), 1, points=points,visualise=True)

    rect = Rect((-20, 20), (40, 120))
    print('-' * 50)
    (ktree.find_points_in(rect))
    (qtree.find_points_in(rect))

test6()
#test2()
#test5()
