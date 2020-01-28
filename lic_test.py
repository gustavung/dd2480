import unittest
import json
import main


class LICTestCase(unittest.TestCase):

    """
    Test case for LIC2 function in module 'main'
    """
    def test_LIC2(self):
        main.PARAMETERS_T["EPSILON"] = 0.5  # Tests NUMPOINTS < 3
        main.POINTS = [
            (0, 0), (1, -1)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertFalse(main.LIC2())

        main.PARAMETERS_T["EPSILON"] = 0.87
        main.POINTS = [
            (2, 3), (1, 4), (0, 0), (3, 3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertTrue(main.LIC2())

        main.PARAMETERS_T["EPSILON"] = 0.2
        main.POINTS = [
            (0, 1), (0, 0), (0, -1)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertFalse(main.LIC2())

        main.PARAMETERS_T["EPSILON"] = 0.2 # Tests invalid angle
        main.POINTS = [
            (1, 1), (0, 0), (0, 0)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertFalse(main.LIC2())


    """
    Test case for LIC8 function in module 'main'
    """
    def test_LIC7(self):

        main.PARAMETERS_T["LENGTH1"] = 1  # Tests NUMPOINTS < 3
        main.PARAMETERS_T["K_PTS"] = 1
        main.POINTS = [
            (0, 0), (2, 2)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertFalse(main.LIC7())

        main.PARAMETERS_T["LENGTH1"] = 1
        main.PARAMETERS_T["K_PTS"] = 2
        main.POINTS = [
            (0, 0), (2, 2), (0, 0), (3, 3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertTrue(main.LIC12())

        main.PARAMETERS_T["LENGTH1"] = 2
        main.PARAMETERS_T["K_PTS"] = 2
        main.POINTS = [
            (0, 0), (2, 2), (0, 0), (3,3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertFalse(main.LIC12())

    """
    Test case for LIC9 function in module 'main'
    """
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

    """
       Test case for LIC12 function in module 'main'
    """
    def test_LIC12(self):

        main.PARAMETERS_T["LENGTH1"] = 1  # Tests NUMPOINTS < 3
        main.PARAMETERS_T["LENGTH2"] = 1
        main.PARAMETERS_T["K_PTS"] = 1
        main.POINTS = [
            (0, 0), (1, -1)]
        main.NUMPOINTS = len(main.POINTS)

        self.assertFalse(main.LIC12())

        main.PARAMETERS_T["LENGTH1"] = 1
        main.PARAMETERS_T["LENGTH2"] = 4
        main.PARAMETERS_T["K_PTS"] = 2
        main.POINTS = [
            (0, 0), (0, 0), (0, 0), (3, 3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertTrue(main.LIC12())

        main.PARAMETERS_T["LENGTH1"] = 1
        main.PARAMETERS_T["LENGTH2"] = 1
        main.PARAMETERS_T["K_PTS"] = 1
        main.POINTS = [
            (0, 0), (2, 2), (0, 0), (3,3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertFalse(main.LIC12())

        main.PARAMETERS_T["LENGTH1"] = 5
        main.PARAMETERS_T["LENGTH2"] = 5
        main.PARAMETERS_T["K_PTS"] = 1
        main.POINTS = [
            (0, 0), (2, 2), (0, 0), (3, 3)]
        main.NUMPOINTS = len(main.POINTS)
        self.assertTrue(main.LIC12())

if __name__ == '__main__':
    unittest.main()