import json
import math

f = open("global.json")
inp = json.load(f)

NUMPOINTS = inp["NUMPOINTS"]
POINTS = inp["POINTS"]
PARAMETERS_T = inp["PARAMETERS_T"]
Q_PTS = PARAMETERS_T["Q_PTS"]
QUADS = PARAMETERS_T["QUADS"]
LCM = inp["LCM"]
PUV = inp["PUV"]

###################### Main entrypoint ######################

"""Return the Conditions Met Vector

This function is a helper stub for mapping and running the correct LIC.
"""
def generate_LIC():
    CMV = [False for _ in range(0, 15)]
    CMV[0]  =    LIC0()
    CMV[1]  =    False#LIC1()
    CMV[2]  =    False#LIC2()
    CMV[3]  =    False#LIC3()
    CMV[4]  =    LIC4()
    CMV[5]  =    LIC5()
    CMV[6]  =    False#LIC6()
    CMV[7]  =    False#LIC7()
    CMV[8]  =    False#LIC8()
    CMV[9]  =    False#LIC9()
    CMV[10] =    LIC10()
    CMV[11] =    False#LIC11()
    CMV[12] =    False#LIC12()
    CMV[13] =    False#LIC13()
    CMV[14] =    False#LIC14()
    return CMV

"""
This function creates Launch Interceptor Condition (LIC) number 0.
Returns true if requirements are met.

The requirements for LIC 0:

There exists at least one set of two consecutive data points that are a distance greater than the length, LENGTH1, apart.
(0 ≤ LENGTH1)
"""

def get_length(i):

    return math.sqrt((POINTS[i][0] - POINTS[i+1][0])**2 + (POINTS[i][1] - POINTS[i+1][1])**2)


def LIC0():

    LENGTH1 = PARAMETERS_T["LENGTH1"]

    for i in range(NUMPOINTS-1):
        if get_length(i) > LENGTH1:
            return True
            
    return False


"""
This function creates Launch Interceptor Condition (LIC) number 4.
Returns true if requirements are met.
The requirements for LIC 4:

There exist at least one set of Q_PTS consecutive data points that lie in more than QUADS quadrants.

"""
def LIC4():
    quads_check = [False for _ in range(0, 4)]
    c_list = []
    if 2 <= Q_PTS <= NUMPOINTS and 1 <= QUADS <= 3:
        for i in range(0, NUMPOINTS - Q_PTS + 1):
            c_list.append(POINTS[i:i + Q_PTS])

        for i in range(0, len(c_list)):
            for j in range(0, Q_PTS):
                if c_list[i][j][0] >= 0 and c_list[i][j][1] >= 0:
                    quads_check[0] = True
                elif c_list[i][j][0] <= -1 and c_list[i][j][1] >= 0:
                    quads_check[1] = True
                elif c_list[i][j][0] <= 0 and c_list[i][j][1] <= -1:
                    quads_check[2] = True
                elif c_list[i][j][0] >= 1 and c_list[i][j][1] <= -1:
                    quads_check[3] = True

            if len([i for i in range(0, len(quads_check)) if quads_check[i] is True]) > QUADS:
                return True
            else:
                quads_check = [False for _ in range(0, 4)]
    return False


"""
This function creates Launch Interceptor Condition (LIC) number 5.
Returns true if requirements are met.

The requirements for LIC 5:

There exists at least one set of two consecutive data points, (X[i],Y[i]) and (X[j],Y[j]), such
that X[j] - X[i] < 0. (where i = j-1)
"""

def LIC5():

    for j in range(1,NUMPOINTS):
        if POINTS[j][0] < POINTS[j-1][0]:
            return True
            
    return False


"""
This function creates Launch Interceptor Condition (LIC) number 10.
Returns true if requirements are met.

The requirements for LIC 10:

There exists at least one set of three data points separated by exactly E_PTS and F_PTS consecutive intervening points, 
respectively, that are the vertices of a triangle with area greater than AREA1. The condition is not met when NUMPOINTS < 5.
1≤E_PTS,1≤F_PTS
E_PTS+F_PTS ≤ NUMPOINTS−3
"""


def triangle_area(i, j, k):

    x1, y1 = POINTS[i][0], POINTS[i][1]
    x2, y2 = POINTS[j][0], POINTS[j][1]
    x3, y3 = POINTS[k][0], POINTS[k][1]

    return abs(0.5 * (((x2-x1)*(y3-y1))-((x3-x1)*(y2-y1))))


def LIC10():

    if NUMPOINTS < 5:
        return False
    
    E_PTS = PARAMETERS_T["E_PTS"]
    F_PTS = PARAMETERS_T["F_PTS"]
    AREA1 = PARAMETERS_T["AREA1"]

    for i in range(NUMPOINTS-E_PTS-F_PTS-2):
        j = i + E_PTS + 1
        k = j + F_PTS + 1

        if triangle_area(i, j, k) > AREA1:
            return True
            
    return False


"""Return a tuple of the launch decision, CMV, PUM and FUV

This function will calculate the necessary control vectors and matrices
as well as deciding whether the missile should launch or not.
The decision will be printed as NO or YES on standard output.
"""
def decide():
    CMV = generate_LIC()
    PUM = [[False for _ in range(0, 15)] for _ in range (0, 15)]
    FUV = [False for _ in range(0, 15)]

    for i in range(0, 15):
        for j in range(0,15):
            if LCM[i][j] == 'ANDD':
                PUM[i][j] = CMV[i] and CMV[j]
            elif LCM[i][j] == 'ORR':
                PUM[i][j] = CMV[i] or CMV[j]
            else:
                PUM[i][j] = True

    for i in range(0, 15):
        FUV[i] = (PUV is False) or all(PUM[i])

    LAUNCH = all(FUV)
    if LAUNCH:
        print("YES")
    else:
        print ("NO")

    return (LAUNCH, CMV, PUM, FUV)


if __name__ == "__name__":
    decide()
