import json
import math

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
Q_PTS = PARAMETERS_T["Q_PTS"]
QUADS = PARAMETERS_T["QUADS"]
AREA1 = PARAMETERS_T["AREA1"]
AREA2 = PARAMETERS_T["AREA2"]
RADIUS1 = PARAMETERS_T["RADIUS1"]
RADIUS2 = PARAMETERS_T["RADIUS2"]

LCM = inp["LCM"]
PUV = inp["PUV"]

###################### Main entrypoint ######################

#Helper function used in LIC8() and LIC13()
#Input: Three points (x,y) and a radius.
#Output: True if the points can be contained in a circle with the radius
def can_be_contained_circle(p1, p2, p3, radius):
    a = euclidian_dist(p1, p2);
    b = euclidian_dist(p1, p3);
    c = euclidian_dist(p2, p3);
    if(a == 0 or b == 0 or c == 0):
        return max([a,b,c])/2 < radius #two or more points are equal

    A = math.acos((b*b + c*c - a*a)/(2*b*c))
    B = math.acos((a*a + c*c - b*b)/(2*a*c))
    C = math.acos((b*b + a*a - c*c)/(2*b*a))
    if(A > PI/2 or B > PI/2 or C > PI/2):
        #triangle is obtuse
        #take longest distance, set center of circle in the middle of it.
        #Compare radius = max distance / 2 with radius.
        return max([a,b,c])/2 < radius
    else:
        #triangle is acute
        #calculate the circumradius of the triangle. Found formula online:
        #https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        r = a/(2*math.sin(A))
        return r < radius

#Helper function
def euclidian_dist(p1, p2):
    return math.sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1] - p2[1], 2)); #sqrt(dx^2 + dy^2)

"""Return the Conditions Met Vector

This function is a helper stub for mapping and running the correct LIC.
"""
def generate_LIC():
    CMV = [False for _ in range(0, 15)]
    CMV[0]  =    False#LIC0()
    CMV[1]  =    False#LIC1()
    CMV[2]  =    False#LIC2()
    CMV[3]  =    False#LIC3()
    CMV[4]  =    LIC4()
    CMV[5]  =    False#LIC5()
    CMV[6]  =    False#LIC6()
    CMV[7]  =    False#LIC7()
    CMV[8]  =    False#LIC8()
    CMV[9]  =    LIC9()
    CMV[10] =    False#LIC10()
    CMV[11] =    False#LIC11()
    CMV[12] =    False#LIC12()
    CMV[13] =    False#LIC13()
    CMV[14] =    LIC14()
    return CMV

def LIC3():
    for i in list(zip(POINTS[:], POINTS[1:], POINTS[2:])):
        [[x1,y1], [x2,y2], [x3,y3]] = i
        #SHOELACE FORMULA for area: https://en.wikipedia.org/wiki/Shoelace_formula
        A = abs(1.0*(x1*y2 + x2*y3 + x3*y1 - x1*y3 - x2*y1 - x3*y2))/2
        if A <= AREA1:
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

def LIC8():
    if NUMPOINTS < 5:
        return False
    for i in list(zip(POINTS[:], POINTS[A_PTS:], POINTS[A_PTS + B_PTS:])):
        [p1, p2, p3] = i
        if(not(can_be_contained_circle(p1,p2,p3,RADIUS1))):
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

def LIC13():
    if NUMPOINTS < 5 or not(LIC8()): #criteria 1 is equal to LIC8
        return False
    for i in list(zip(POINTS[:], POINTS[A_PTS:], POINTS[A_PTS + B_PTS:])):
        [p1, p2, p3] = i
        if(can_be_contained_circle(p1,p2,p3,RADIUS2)): #critera 2
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
