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
N_PTS = PARAMETERS_T["N_PTS"]
Q_PTS = PARAMETERS_T["Q_PTS"]
QUADS = PARAMETERS_T["QUADS"]
AREA1 = PARAMETERS_T["AREA1"]
AREA2 = PARAMETERS_T["AREA2"]
DIST = PARAMETERS_T["DIST"]
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

def get_length(i):
    """ Computes the euclidean distance between two points given an index.
    """
    return math.sqrt((POINTS[i][0] - POINTS[i+1][0])**2 + (POINTS[i][1] - POINTS[i+1][1])**2)

def triangle_area(i, j, k):
    """ Computes the area of a triangle given some indices.
    """
    x1, y1 = POINTS[i][0], POINTS[i][1]
    x2, y2 = POINTS[j][0], POINTS[j][1]
    x3, y3 = POINTS[k][0], POINTS[k][1]

    return abs(0.5 * (((x2-x1)*(y3-y1))-((x3-x1)*(y2-y1))))

def twelvefirst():
    """ Determine if the first condition of LIC12 is fulfilled.
        True if there exists at least one set of two data points, separated by exactly K_PTS consecutive intervening points,
        which are a distance greater than the length, LENGTH1, apart.
    """
    i = 0
    j = NUMPOINTS
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
    j = NUMPOINTS
    while i < j and i+K_PTS < j:
        (x1, x2) = POINTS[i], POINTS[i + K_PTS]
        if euclidean_dist(x1, x2) < LENGTH2:
            return True
        i = i+1
    return False

def can_be_contained_circle(p1, p2, p3, radius):
    """ Helper function used in LIC6, LIC8 and LIC13.
        Input: Three points (x,y) and a radius.
        Output: True if the points can be contained in a circle with the radius.
    """
    a = euclidean_dist(p1, p2);
    b = euclidean_dist(p1, p3);
    c = euclidean_dist(p2, p3);
    if(a == 0 or b == 0 or c == 0):
        return max([a,b,c])/2 <= radius #two or more points are equal

    A = math.acos((b*b + c*c - a*a)/(2*b*c))
    B = math.acos((a*a + c*c - b*b)/(2*a*c))
    C = math.acos((b*b + a*a - c*c)/(2*b*a))
    if(A > PI/2 or B > PI/2 or C > PI/2):
        #triangle is obtuse
        #take longest distance, set center of circle in the middle of it.
        #Compare radius = max distance / 2 with radius.
        return max([a,b,c])/2 <= radius
    else:
        #triangle is acute
        #calculate the circumradius of the triangle. Found formula online:
        #https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        r = a/(2*math.sin(A))
        return r <= radius

def dist_to_line(p1, p2, p3):
    """ Calculates the distance between a line defined by p1 and p2 and a third point p3.
        It does this by calculating the length of the rejection of the line p3-p1 and p2-p1.
    """

    (x1, y1) = p1
    (x2, y2) = p2
    (x3, y3) = p3

    numer = abs((y2-y1)*x3 - (x2-x1)*y3 + x2*y1 - y2*x1)
    denom = math.sqrt(math.pow(y2-y1, 2) + math.pow(x2-x1, 2))
    return numer/denom

def generate_LIC():
    """ Return the Conditions Met Vector.
        This function is a helper stub for mapping and running the correct LIC.
    """
    CMV = [False for _ in range(0, 15)]
    CMV[0]  =    LIC0()
    CMV[1]  =    LIC1()
    CMV[2]  =    LIC2()
    CMV[3]  =    LIC3()
    CMV[4]  =    LIC4()
    CMV[5]  =    LIC5()
    CMV[6]  =    LIC6()
    CMV[7]  =    LIC7()
    CMV[8]  =    LIC8()
    CMV[9]  =    LIC9()
    CMV[10] =    LIC10()
    CMV[11] =    LIC11()
    CMV[12] =    LIC12()
    CMV[13] =    LIC13()
    CMV[14] =    LIC14()
    return CMV

def LIC0():
    """
    This function creates Launch Interceptor Condition (LIC) number 0.
    Returns true if requirements are met.

    The requirements for LIC 0:

    There exists at least one set of two consecutive data points that are a distance greater than the length, LENGTH1, apart.
    (0 ≤ LENGTH1)
    """
    LENGTH1 = PARAMETERS_T["LENGTH1"]

    for i in range(NUMPOINTS-1):
        if get_length(i) > LENGTH1:
            return True

    return False

def LIC1():
    """ Determine if the Launch Interceptor Condition (LIC) number 1 is fulfilled.
        Is true iff there exists at least one set of three consecutive data points that cannot all be contained
        within or on a circle of radius RADIUS1.
    """
    assert RADIUS1 >= 0
    for point_seq in zip(POINTS[:-1], POINTS[1:-1], POINTS[2:]):
        (p1, p2, p3) = point_seq
        if not (can_be_contained_circle(p1, p2, p3, RADIUS1)):
            return True
    return False

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

def LIC3():
    """ This function creates Launch Interceptor Condition (LIC) number 3.
        Returns true if requirements are met.
        The requirements for LIC 3:
        There exists at least one set of three consecutive data points that are the vertices of a triangle
        with area greater than AREA1. (0 <= AREA1)
    """
    for [[x1,y1], [x2,y2], [x3,y3]] in list(zip(POINTS[:], POINTS[1:], POINTS[2:])):
        #SHOELACE FORMULA for area: https://en.wikipedia.org/wiki/Shoelace_formula
        A = abs(1.0*(x1*y2 + x2*y3 + x3*y1 - x1*y3 - x2*y1 - x3*y2))/2
        if A <= AREA1:
            return True
    return False

def LIC4():
    """
    This function creates Launch Interceptor Condition (LIC) number 4.
    Returns true if requirements are met.
    The requirements for LIC 4:
    There exist at least one set of Q_PTS consecutive data points that lie in more than QUADS quadrants.
    """
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


def LIC5():
    """
    This function creates Launch Interceptor Condition (LIC) number 5.
    Returns true if requirements are met.

    The requirements for LIC 5:

    There exists at least one set of two consecutive data points, (X[i],Y[i]) and (X[j],Y[j]), such
    that X[j] - X[i] < 0. (where i = j-1)
    """
    for j in range(1,NUMPOINTS):
        if POINTS[j][0] < POINTS[j-1][0]:
            return True

    return False

def LIC6():
    """ Determine if the Launch Interceptor Condition (LIC) number 6 is fulfilled.
        There exists at least one set of N_PTS consecutive data points such that at least one of the
        points lies a distance greater than DIST from the line joining the first and last of these N_PTS
        points. If the first and last points of these N_PTS are identical, then the calculated distance
        to compare with DIST will be the distance from the coincident point to all other points of
        the N_PTS consecutive points. The condition is not met when NUMPOINTS < 3.
    """
    if NUMPOINTS < 3:
        return False
    assert DIST >= 0
    condition_set = []
    for i in range(0, NUMPOINTS-(N_PTS-1)):
        points = POINTS[i:i+N_PTS]
        if points[0] == points[-1]:
            condition_set = list(filter(lambda p: euclidean_dist(points[0], p) > DIST, points[1:-1]))
        else:
            condition_set = list((filter(lambda p: dist_to_line(points[0], points[-1], p) > DIST, points[1:-1])))
        if len(condition_set) > 0:
            return True
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

def LIC8():
    """ This function creates Launch Interceptor Condition (LIC) number 8.
        Returns true if requirements are met.
        The requirements for LIC 8:
        There exists at least one set of three data points separated by exactly A PTS and B PTS consecutive
        intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1.
        The condition is not met when NUMPOINTS < 5.
        1 <= A_PTS , 1 <= B PTS
        A_PTS + B_PTS <= (NUMPOINTS-3)
    """
    if NUMPOINTS < 5:
        return False
    for [p1, p2, p3] in list(zip(POINTS[:], POINTS[A_PTS:], POINTS[A_PTS + B_PTS:])):
        if(not(can_be_contained_circle(p1,p2,p3,RADIUS1))):
            return True
    return False

def LIC9():
    """
    This function creates Launch Interceptor Condition (LIC) number 9.
    Return True if requirements is met.
    The requirements for LIC 9:
    There exist at least one set of three data points separated by exactly C_PTS and D_PTS
    consecutive intervening points that forms an angle.

    """
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

def LIC10():
    """
    This function creates Launch Interceptor Condition (LIC) number 10.
    Returns true if requirements are met.

    The requirements for LIC 10:

    There exists at least one set of three data points separated by exactly E_PTS and F_PTS consecutive intervening points,
    respectively, that are the vertices of a triangle with area greater than AREA1. The condition is not met when NUMPOINTS < 5.
    1≤E_PTS,1≤F_PTS
    E_PTS+F_PTS ≤ NUMPOINTS−3
    """
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

def LIC11():
    """ Determine if the Launch Interceptor Condition (LIC) number 11 is fulfilled.
        There exists at least one set of two data points, (X[i],Y[i]) and (X[j],Y[j]), separated by
        exactly G PTS consecutive intervening points, such that X[j] - X[i] < 0. (where i < j ) The
        condition is not met when NUMPOINTS < 3.
    """
    if NUMPOINTS < 3:
        return False
    assert 1 <= G_PTS <= NUMPOINTS
    for i in range(0, NUMPOINTS-(G_PTS+1)):
        if POINTS[i+G_PTS+1][0]-POINTS[i][0] < 0:
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

def LIC13():
    """ This function creates Launch Interceptor Condition (LIC) number 13.
        Returns true if requirements are met.
        The requirements for LIC 13:

        There exists at least one set of three data points, separated by exactly A PTS and B PTS consecutive
        intervening points, respectively, that cannot be contained within or on a circle of radius RADIUS1.
        In addition, there exists at least one set of three data points (which can be the same or different
        from the three data points just mentioned) separated by exactly A PTS and B PTS consecutive
        intervening points, respectively, that can be contained in or on a circle of radius RADIUS2. Both
        parts must be true for the LIC to be true. The condition is not met when NUMPOINTS < 5.
        0 <= RADIUS2
    """
    if NUMPOINTS < 5 or not(LIC8()): #criteria 1 is equal to LIC8
        return False
    for [p1, p2, p3] in list(zip(POINTS[:], POINTS[A_PTS:], POINTS[A_PTS + B_PTS:])):
        if(can_be_contained_circle(p1,p2,p3,RADIUS2)): #critera 2
            return True
    return False

def LIC14():
    """
    This function creates Launch Interceptor Condition (LIC) number 14.
    Return True if requirements is met.
    The requirements for LIC 14:

    There exist at least one set of three data points,
    separated by exactly E_PTS and F_PTS consecutive intervening points
    that are the vertices of a triangle with area greater then AREA1 and AREA2

    """
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
        print("NO")

    return LAUNCH

if __name__ == "__main__":
    decide()
