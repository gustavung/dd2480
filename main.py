import json
import math
import numpy as np

f = open("global.json")
inp = json.load(f)

NUMPOINTS = inp["NUMPOINTS"]
POINTS = inp["POINTS"]
PARAMETERS_T = inp["PARAMETERS_T"]
PI = inp["PI"]
EPSILON = PARAMETERS_T["EPSILON"]
A_PTS = PARAMETERS_T["A_PTS"]
B_PTS = PARAMETERS_T["B_PTS"]
C_PTS = PARAMETERS_T["C_PTS"]
D_PTS = PARAMETERS_T["D_PTS"]
E_PTS = PARAMETERS_T["E_PTS"]
F_PTS = PARAMETERS_T["F_PTS"]
G_PTS = PARAMETERS_T["G_PTS"]
K_PTS = PARAMETERS_T["K_PTS"]
Q_PTS = PARAMETERS_T["Q_PTS"]
QUADS = PARAMETERS_T["QUADS"]
AREA1 = PARAMETERS_T["AREA1"]
AREA2 = PARAMETERS_T["AREA2"]
RADIUS1 = PARAMETERS_T["RADIUS1"]
RADIUS2 = PARAMETERS_T["RADIUS2"]
LENGTH1 = PARAMETERS_T["LENGTH1"]
LENGTH2 = PARAMETERS_T["LENGTH2"]
LCM = inp["LCM"]
PUV = inp["PUV"]

###################### Main entrypoint ######################

def euclidean_dist(p1, p2):
    """ Computes the euclidean distance between two points
    """
    return math.sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1] - p2[1], 2)); #sqrt(dx^2 + dy^2)

def twelvefirst():
    """ Determine if the first condition of LIC12 is fulfilled.
        True if there exists at least one set of two data points, separated by exactly K_PTS consecutive intervening points,
        which are a distance greater than the length, LENGTH1, apart.
    """
    i = 0
    j = NUMPOINTS-1
    while i < j and i+K_PTS < j:
        (x1, x2) = POINTS[i], POINTS[i+K_PTS]
        if euclidean_dist(x1, x2) > LENGTH1:
            return True
        i = i+1
    return False

def twelvesecond():
    """ Determine if the second condition of LIC12 is fulfilled.
        True if there exists at least one set of two data points (which can be the same or different from
        the two data points just mentioned), separated by exactly K_PTS consecutive intervening
        points, that are a distance less than the length, LENGTH2, apart.
    """
    i = 0
    j = NUMPOINTS-1
    while i < j and i+K_PTS < j:
        (x1, x2) = POINTS[i], POINTS[i + K_PTS]
        if euclidean_dist(x1, x2) < LENGTH2:
            return True
        i = i+1
    return False

def generate_LIC():
    """ Return the Conditions Met Vector.
        This function is a helper stub for mapping and running the correct LIC.
    """
    CMV = [False for _ in range(0, 15)]
    CMV[0]  =    False#LIC0()
    CMV[1]  =    False#LIC1()
    CMV[2]  =    LIC2()
    CMV[3]  =    False#LIC3()
    CMV[4]  =    False#LIC4()
    CMV[5]  =    False#LIC5()
    CMV[6]  =    False#LIC6()
    CMV[7]  =    LIC7()
    CMV[8]  =    False#LIC8()
    CMV[9]  =    False#LIC9()
    CMV[10] =    False#LIC10()
    CMV[11] =    False#LIC11()
    CMV[12] =    LIC12()
    CMV[13] =    False#LIC13()
    CMV[14] =    False#LIC14()
    return CMV

def LIC2():
    """ Determine if the Launch Interceptor Condition (LIC) number 2 is fulfilled.
        Is true if there exists at least one set of three consecutive data points which form an angle such that:
        angle < (PI−EPSILON) or angle > (PI+EPSILON) and the angle is defined.
    """
    i = 0
    j = NUMPOINTS-1
    while i < j and i + 2 < j:
        (x1, x2) = POINTS[i][0], POINTS[i][1]
        (y1, y2) = POINTS[i+1][0], POINTS[i+1][1]
        (z1, z2) = POINTS[i+2][0], POINTS[i+2][1]
        if (x1 == y1 and x2 == y2) or (z1 == y1 and z2 == y2): # Checks that the angle is defined
            i = i+1
            continue
        angle = math.atan2(z2-y2, z1-y1)-math.atan2(x2-y2, x1-y1)
        if angle < 0:
            angle = angle + PI*2
        if angle < PI-EPSILON or angle > PI+EPSILON:
            return True
        i = i + 1
    return False

def LIC7():
    """"
    There exists at least one set of two data points separated by exactly K_PTS consecutive intervening points that are a
     distance greater than the length, LENGTH1, apart. The condition is not met when NUMPOINTS < 3.
    1 ≤ K_PTS ≤ (NUMPOINTS − 2)
    """
    if twelvefirst() and NUMPOINTS-1 >= 3:
        return True
    return False

def LIC12():
    """"
    Determine if the Launch Interceptor Condition (LIC) number 12 is fulfilled.
    True if there exists at least one set of two data points, separated by exactly K_PTS consecutive
    intervening points, which are a distance greater than the length, LENGTH1, apart. In addi-
    tion, there exists at least one set of two data points (which can be the same or different from
    the two data points just mentioned), separated by exactly K_PTS consecutive intervening
    points, that are a distance less than the length, LENGTH2, apart. Both parts must be true
    for the LIC to be true. The condition is not met when NUMPOINTS < 3.
    """
    if twelvefirst() and twelvesecond() and NUMPOINTS-1 >= 3:
        return True
    return False

def decide():
    """Return a tuple of the launch decision, CMV, PUM and FUV
	This function will calculate the necessary control vectors and matrices
	as well as deciding whether the missile should launch or not.
	The decision will be printed as NO or YES on standard output.
    """
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
        FUV[i] = (PUV[i] is False) or all(PUM[i])

    LAUNCH = all(FUV)
    if LAUNCH:
        print("YES")
    else:
        print ("NO")

    return (LAUNCH, CMV, PUM, FUV)

if __name__ == "__name__":
    decide()