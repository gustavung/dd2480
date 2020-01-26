import json
import math

f = open("global.json")
inp = json.load(f)

NUMPOINTS = inp["NUMPOINTS"]
POINTS = inp["POINTS"]
PARAMETERS_T = inp["PARAMETERS_T"]
PI = inp["PI"]
EPSILON = PARAMETERS_T["EPSILON"]
C_PTS = PARAMETERS_T["C_PTS"]
D_PTS = PARAMETERS_T["D_PTS"]
E_PTS = PARAMETERS_T["E_PTS"]
F_PTS = PARAMETERS_T["F_PTS"]
Q_PTS = PARAMETERS_T["Q_PTS"]
QUADS = PARAMETERS_T["QUADS"]
AREA1 = PARAMETERS_T["AREA1"]
AREA2 = PARAMETERS_T["AREA2"]
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
    CMV[9]  =    LIC9()
    CMV[10] =    LIC10()
    CMV[11] =    False#LIC11()
    CMV[12] =    False#LIC12()
    CMV[13] =    False#LIC13()
    CMV[14] =    LIC14()
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


"""
This function creates Launch Interceptor Condition (LIC) number 9.
Return True if requirements is met.
The requirements for LIC 9:

There exist at least one set of three data points separated by exactly C_PTS and D_PTS
consecutive intervening points that forms an angle.

"""
def LIC9():
    if NUMPOINTS > 5 and 1 <= C_PTS and 1 <= D_PTS and (C_PTS + D_PTS) <= (NUMPOINTS-3):
        for i in range(0, NUMPOINTS-2-C_PTS-D_PTS):
            a = POINTS[i]                   # Point a
            v = POINTS[i+1+C_PTS]           # Vertex
            b = POINTS[i+2+C_PTS+D_PTS]     # Point b

            if a != v and b != v:
                va = ((a[0] - v[0]), (a[1] - v[1]))  # Vector from vertex v to point a
                vb = ((b[0] - v[0]), (b[1] - v[1]))  # Vector from vertex v to point b

                dp = va[0] * vb[0] + va[1] * vb[1]  # Dot product of vector va and vb

                ma = math.sqrt(sum(i ** 2 for i in va))  # Magnitude vector va
                mb = math.sqrt(sum(i ** 2 for i in vb))  # Magnitude vector vb

                angle = math.acos(dp / (ma * mb))   # Angle in radians

                if angle < (PI - EPSILON) or angle > (PI + EPSILON):
                    return True

    return False


"""
This function creates Launch Interceptor Condition (LIC) number 14.
Return True if requirements is met.
The requirements for LIC 14:

There exist at least one set of three data points, 
separated by exactly E_PTS and F_PTS consecutive intervening points
that are the vertices of a triangle with area greater then AREA1 and AREA2

"""
def LIC14():
    condition = [False, False]
    if NUMPOINTS > 5 and 0 <= AREA1 and 0 <= AREA2:

        for i in range(0, NUMPOINTS-2-E_PTS-F_PTS):
            a = POINTS[i]                   # Point a
            b = POINTS[i+1+E_PTS]           # Point b
            c = POINTS[i+2+E_PTS+F_PTS]     # Point c

            area = abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))

            if area > AREA1:
                condition[0] = True
            if area > AREA2:
                condition[1] = True

        return condition[0] and condition[1]

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
