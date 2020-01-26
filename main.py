import json
import math

f = open("global.json")
inp = json.load(f)
PI = inp["PI"]
NUMPOINTS = inp["NUMPOINTS"]
POINTS = inp["POINTS"]
PARAMETERS_T = inp["PARAMETERS_T"]
LCM = inp["LCM"]
PUV = inp["PUV"]
RADIUS1 = PARAMETERS_T["RADIUS1"]
RADIUS2 = PARAMETERS_T["RADIUS2"]
A_PTS = PARAMETERS_T["A_PTS"]
B_PTS = PARAMETERS_T["B_PTS"]

###################### Main entrypoint ######################

def LIC3():
    for i in list(zip(POINTS[:], POINTS[1:], POINTS[2:])):
        [[x1,y1], [x2,y2], [x3,y3]] = i
        #SHOELACE FORMULA for area: https://en.wikipedia.org/wiki/Shoelace_formula
        A = abs(1.0*(x1*y2 + x2*y3 + x3*y1 - x1*y3 - x2*y1 - x3*y2))/2
        if A <= AREA1:
            return True
    return False

def LIC8():
    if NUMPOINTS < 5:
        return False
    for i in list(zip(POINTS[:], POINTS[A_PTS:], POINTS[A_PTS + B_PTS:])):
        [p1, p2, p3] = i
        if(not(can_be_contained_circle(p1,p2,p3,RADIUS1))):
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
    CMV[4]  =    False#LIC4()
    CMV[5]  =    False#LIC5()
    CMV[6]  =    False#LIC6()
    CMV[7]  =    False#LIC7()
    CMV[8]  =    False#LIC8()
    CMV[9]  =    False#LIC9()
    CMV[10] =    False#LIC10()
    CMV[11] =    False#LIC11()
    CMV[12] =    False#LIC12()
    CMV[13] =    False#LIC13()
    CMV[14] =    False#LIC14()
    return CMV

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

decide()
