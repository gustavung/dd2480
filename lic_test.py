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

    def test_LIC8(self):
        main.RADIUS1 = 0
        main.POINTS = [[0,0],[-1,-1],[-1,-1],[1,0],[1,2]]
        main.NUMPOINTS = len(main.POINTS)
        main.A_PTS = 3
        main.B_PTS = 1
        self.assertTrue(main.LIC8())
        main.RADIUS1 = 2
        self.assertFalse(main.LIC8())

    def test_LIC13(self):
        main.RADIUS1 = 0
        main.POINTS = [[0,0],[-1,-1],[-1,-1],[1,0],[1,2]]
        main.NUMPOINTS = len(main.POINTS)
        main.A_PTS = 3
        main.B_PTS = 1
        self.assertFalse(main.LIC13())


if __name__ == '__main__':
    unittest.main()
