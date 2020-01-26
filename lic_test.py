import unittest
import json
import main


class LICTestCase(unittest.TestCase):

    def test_LIC3(self):
        main.AREA1 = 1
        main.POINTS = [[0,0],[1,0],[1,2]] # ==> area = 1
        main.NUMPOINTS = len(main.POINTS)

        self.assertTrue(main.LIC3())
        main.AREA1 = 0
        self.assertFalse(main.LIC3())

        main.POINTS = [[0,0],[1,0],[1,100]] # ==> area = 50
        main.AREA1 = 51
        self.assertTrue(main.LIC3())
        main.AREA1 = 49
        self.assertFalse(main.LIC3())

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

    def test_LIC8(self):
        main.RADIUS1 = 0
        main.POINTS = [[0,0],[-1,-1],[-1,-1],[1,0],[1,2]]
        main.NUMPOINTS = len(main.POINTS)
        main.A_PTS = 3
        main.B_PTS = 1
        self.assertTrue(main.LIC8())
        main.RADIUS1 = 2
        self.assertFalse(main.LIC8())

    def test_lic9(self):

        main.POINTS = [
            (3, 3), (-12, 19), (1, 1),
            (51, 91), (1, 3), (99, 99)
            ]
        main.NUMPOINTS = len(main.POINTS)
        main.C_PTS = 1
        main.D_PTS = 1
        main.EPSILON = 2.1
        main.PI = 3.1415926535
        self.assertTrue(main.LIC9())

        main.EPSILON = 4
        self.assertFalse(main.LIC9())

        main.EPSILON = 2.1
        main.D_PTS = 3
        self.assertFalse(main.LIC9())

    def test_LIC13(self):
        main.RADIUS1 = 0
        main.POINTS = [[0,0],[-1,-1],[-1,-1],[1,0],[1,2]]
        main.NUMPOINTS = len(main.POINTS)
        main.A_PTS = 3
        main.B_PTS = 1
        self.assertFalse(main.LIC13())

    def test_lic14(self):
        main.E_PTS = 1
        main.F_PTS = 1
        main.NUMPOINTS = 5

        self.assertFalse(main.LIC14())

        main.POINTS = [
                (3, 3), (-12, 19), (1, 1),
                (51, 91), (1, 3), (99, 99)
            ]
        main.NUMPOINTS = len(main.POINTS)
        main.AREA1 = 4
        main.AREA2 = 400

        self.assertTrue(main.LIC14())

        main.AREA2 = 3000
        self.assertFalse(main.LIC14())

if __name__ == '__main__':
    unittest.main()
