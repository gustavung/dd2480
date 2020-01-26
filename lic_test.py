import unittest
import json
import main


class LICTestCase(unittest.TestCase):


    """
    Test case for LIC5 function in module 'main'
    """
    def test_LIC0(self):
        main.PARAMETERS_T["LENGTH1"] = 30
        main.POINTS = [
            (0, 0), (1, -1), (3, 6), (1, 1),
            (1, 3), (2, 2), (-9, -5), (-1, -5),
            (2, 3), (-1, -5), (0, -2), (2, 2)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertFalse(main.LIC0())

        main.PARAMETERS_T["LENGTH1"] = 17
        main.POINTS = [
            (0, 0), (1, -1), (3, 6), (1, 1),
            (1, 3), (2, 2), (-1, -5), (-1, -5),
            (2, 3), (-1, -5), (0, 0), (8, 15)]

        self.assertFalse(main.LIC0())

        main.POINTS = [
            (0, 0), (1, -1), (3, 6), (1, 1),
            (1, 3), (2, 2), (-9, -5), (-1, -5),
            (2, 3), (-1, -5), (0, 0), (8, 15.1)]

        self.assertTrue(main.LIC0())


    """
    Test case for LIC4 function in module 'main'
    """
    def test_LIC4(self):

        main.Q_PTS = 4
        main.QUADS = 2
        main.POINTS = [
            (7, 8), (-12, 19), (-12, -22), (51, 91),
            (42, 85), (62, 32), (79, 15), (11, 95),
            (2, 73), (70, 50), (60, 32), (28, 24),
            (60, 29), (14, 59), (97, 71), (60, 45),
            (21, 17), (8, 49), (93, 74), (18, 66),
            (23, 26), (25, 44), (78, 40), (31, 25),
            (47, 84), (5, 56), (99, 34), (23, 26)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertTrue(main.LIC4())

        main.Q_PTS = 3
        main.QUADS = 2
        main.POINTS = [
            (7, 8), (-12, 19), (-12, 22), (51, 91),
            (42, 85), (62, 32), (79, 15), (11, 95),
            (2, 73), (-70, -50), (60, -32), (28, 24),
            ]
        main.NUMPOINTS = len(main.POINTS)
        self.assertTrue(main.LIC4())

        main.QUADS = 3
        self.assertFalse(main.LIC4())

        main.Q_PTS = 1
        self.assertFalse(main.LIC4())


    """
    Test case for LIC5 function in module 'main'
    """
    def test_LIC5(self):
        main.POINTS = [
            (0, 0), (1, -1), (3, 6), (3, 1)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertFalse(main.LIC5())

        main.POINTS = [
            (0, 0), (1, -1), (3, 6), (2, 1)]

        self.assertTrue(main.LIC5())

    
    """
    Test case for LIC10 function in module 'main'
    """
    def test_LIC10(self):

        main.PARAMETERS_T["E_PTS"] = 1
        main.PARAMETERS_T["F_PTS"] = 1
        main.PARAMETERS_T["AREA1"] = 0
        main.POINTS = [
            (0, 0), (1, -1), (0, 0), (3, 1), (0, 0)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertFalse(main.LIC10())

        main.PARAMETERS_T["AREA1"] = 18
        main.POINTS = [
            (0, 0), (1, -1), (0, 6), (2, 1), (6.01, 0)]

        self.assertTrue(main.LIC10())


if __name__ == '__main__':
    unittest.main()
