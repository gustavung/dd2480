import unittest
import json
import main


class DecideTestCase(unittest.TestCase):

    def setUpMockData1(self):
        self.testfile1 = open("MockData/mockdata1.json")
        self.inp = json.load(self.testfile1)
        self.setUpGlobalVariables()

    def setUpMockData2(self):
        self.testfile2 = open("MockData/mockdata2.json")
        self.inp = json.load(self.testfile2)
        self.setUpGlobalVariables()

    def setUpMockData3(self):
        self.testfile3 = open("MockData/mockdata3.json")
        self.inp = json.load(self.testfile3)
        self.setUpGlobalVariables()

    def setUpGlobalVariables(self):
        main.NUMPOINTS = self.inp["NUMPOINTS"]
        main.POINTS = self.inp["POINTS"]
        PARAMETERS_T = self.inp["PARAMETERS_T"]
        main.PI = self.inp["PI"]
        main.EPSILON = PARAMETERS_T["EPSILON"]
        main.A_PTS = PARAMETERS_T["A_PTS"]
        main.B_PTS = PARAMETERS_T["B_PTS"]
        main.C_PTS = PARAMETERS_T["C_PTS"]
        main.D_PTS = PARAMETERS_T["D_PTS"]
        main.E_PTS = PARAMETERS_T["E_PTS"]
        main.F_PTS = PARAMETERS_T["F_PTS"]
        main.G_PTS = PARAMETERS_T["G_PTS"]
        main.K_PTS = PARAMETERS_T["K_PTS"]
        main.N_PTS = PARAMETERS_T["N_PTS"]
        main.Q_PTS = PARAMETERS_T["Q_PTS"]
        main.QUADS = PARAMETERS_T["QUADS"]
        main.AREA1 = PARAMETERS_T["AREA1"]
        main.AREA2 = PARAMETERS_T["AREA2"]
        main.DIST = PARAMETERS_T["DIST"]
        main.RADIUS1 = PARAMETERS_T["RADIUS1"]
        main.RADIUS2 = PARAMETERS_T["RADIUS2"]
        main.LENGTH1 = PARAMETERS_T["LENGTH1"]
        main.LENGTH2 = PARAMETERS_T["LENGTH2"]

        main.LCM = self.inp["LCM"]
        main.PUV = self.inp["PUV"]

    def testDecide(self):
        self.setUpMockData1()
        self.testfile1.close()
        self.assertTrue(main.decide())

        self.setUpMockData2()
        self.testfile2.close()
        self.assertTrue(main.decide())

        self.setUpMockData3()
        self.testfile3.close()
        self.assertFalse(main.decide())


if __name__ == '__main__':
    unittest.main()
