import unittest
from kdtree import KDTree
from geometry.Rect import Rect


class TestTrees(unittest.TestCase):
    def test_contains_int(self):
        points = [(10, 85), (18, 89), (29, 33),
                  (32, 76), (34, 21), (39, 69),
                  (43, 94), (44, 74), (60, 48),
                  (61, 49), (61, 90), (66, 6),
                  (69, 60), (71, 72), (84, 49)]

        checkpoints = [(44, 74), (66, 6),
                       (72, 59), (97, 86),
                       (41, 29), (69, 60),
                       (10, 85), (9, 19),
                       (45, 25), (84, 49)]

        results = [True,  True,
                   False, False,
                   False, True,
                   True,  False,
                   False, True]

        tree = KDTree(points)
        # quadtree will be here too

        for checkpoint, expected_result in zip(checkpoints, results):
            # direct call to the method
            self.assertEqual(tree.contains(checkpoint), expected_result,
                             f'{checkpoint} point test failed')
            # call using special class methods
            self.assertEqual(checkpoint in tree, expected_result,
                             f'{checkpoint} point test failed')

    def test_contains_float(self):
        points = [(10.23823, 97.54655), (21.69386, 61.08857), (26.5443, 51.29767),
                  (30.22109, 19.83629), (35.83114, 79.59375), (41.02798, 69.55036),
                  (43.06388, 62.39269), (44.71609, 22.87838), (50.30803, 77.5922),
                  (60.28991, 69.49429), (69.76965, 34.37997), (72.70958, 94.48302),
                  (86.78683, 74.22789), (88.1796, 52.55651),  (93.06464, 56.67088)]

        checkpoints = [(16.185, 80.25312),   (29.37526, 54.58067),
                       (85.70135, 83.52599), (72.70958, 94.48302),
                       (88.1796, 52.55651),  (19.91432, 49.70687),
                       (84.99745, 36.34022), (21.69386, 61.08857),
                       (86.78683, 74.22789), (10.23823, 97.54655)]

        results = [False, False,
                   False, True,
                   True,  False,
                   False, True,
                   True,  True]

        tree = KDTree(points)
        # quadtree will be here too

        for checkpoint, expected_result in zip(checkpoints, results):
            # direct call to the method
            self.assertEqual(tree.contains(checkpoint), expected_result,
                             f'{checkpoint} point test failed')
            # call using special class methods
            self.assertEqual(checkpoint in tree, expected_result,
                             f'{checkpoint} point test failed')

    def test_search_points_int(self):
        points = [(14, 93), (17, 73), (19, 33),
                  (27, 68), (29, 72), (33, 30),
                  (50, 57), (59, 17), (62, 63),
                  (66, 41), (85, 56), (86, 58),
                  (91, 11), (92, 98), (98, 47)]

        rect = Rect((30, 10), (95, 70))

        results = [(33, 30), (50, 57), (59, 17),
                   (62, 63), (66, 41), (85, 56),
                   (86, 58), (91, 11)]

        tree = KDTree(points)
        # quadtree here

        inside = tree.find_points_in(rect)
        self.assertEqual(len(inside), len(results),
                         f'The count of found points does not match the expected')
        for point in inside:
            self.assertTrue(tuple(point.point) in results,
                            f'{point} is not inside the {rect}')

    def test_search_points_float(self):
        points = [(13.0088, 73.47405),  (19.37122, 92.27245), (26.81686, 60.45529),
                  (30.86009, 77.78741), (31.64859, 88.05649), (47.89563, 63.91615),
                  (54.94825, 57.69471), (58.60036, 39.4115),  (66.36514, 72.69857),
                  (69.98282, 24.71197), (71.91889, 40.94198), (81.91302, 87.35569),
                  (89.44507, 18.6295),  (97.43819, 18.13145), (98.47172, 44.33949)]

        rect = Rect((22.123, 15.423), (87.639, 82.873))

        results = [(26.81686, 60.45529), (30.86009, 77.78741),
                   (47.89563, 63.91615), (54.94825, 57.69471),
                   (58.60036, 39.4115),  (66.36514, 72.69857),
                   (69.98282, 24.71197), (71.91889, 40.94198)]

        tree = KDTree(points)
        # quadtree here

        inside = tree.find_points_in(rect)
        self.assertEqual(len(inside), len(results),
                         f'The count of found points does not match the expected')
        for point in inside:
            self.assertTrue(tuple(point.point) in results,
                            f'{point} is not inside the {rect}')


if __name__ == '__main__':
    unittest.main()
