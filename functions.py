#import monkdata as m
import math

AREA1 = 10
myVec = [[1,3],[2,3],[5,6],[3,3],[7,7]]

NUMPOINTS = 10
RADIUS1 = 3.4
RADIUS2 = 100
A_PTS = 2
B_PTS = 2
PI = 3.1415

print list(zip(myVec[:], myVec[2:], myVec[2+2:]))


#There exists at least one set of three consecutive data points
#that are the vertices of a triangle with area greater than AREA1.
def LIC3():
    print "hey there"
    length = len(myVec)-2
    for i in list(zip(myVec[:], myVec[1:], myVec[2:])):
        p1 = i[0]
        p2 = i[1]
        p3 = i[2]

        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x3 = p3[0]
        y3 = p3[1]
        #SHOELACE FORMULA for area: https://en.wikipedia.org/wiki/Shoelace_formula
        A = 1/2*((x2*y3 - x3*y2) - (x1*y3 - x3*y1) + (x1*y2 - x2*y1))
        if A < AREA1:
            return True
    return False
#There exists at least one set of three data points separated by exactly A PTS
#and B PTS consecutive intervening points, respectively, that cannot be contained
#within or on a circle of radius RADIUS1. The condition is not met when NUMPOINTS < 5.
def LIC8():
    if NUMPOINTS < 5:
        return False
    for i in list(zip(myVec[:], myVec[A_PTS:], myVec[A_PTS + B_PTS:])):
        p1 = i[0]
        p2 = i[1]
        p3 = i[2]
        if(not(can_be_contained_circle(p1,p2,p3,RADIUS1))):
            return True
    return False

def LIC13():
    if NUMPOINTS < 5 or not(LIC8()): #criteria 1 is equal to LIC8
        return False
    for i in list(zip(myVec[:], myVec[A_PTS:], myVec[A_PTS + B_PTS:])):
        p1 = i[0]
        p2 = i[1]
        p3 = i[2]
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
    A = math.acos((b*b + c*c - a*a)/(2*b*c))
    B = math.acos((a*a + c*c - b*b)/(2*a*c))
    C = math.acos((b*b + a*a - c*c)/(2*b*a))
    if(A > PI/2 or B > PI/2 or C > PI/2):
        #one angle > 90 degrees ==> triangle is obtuse
        #take longest distance, set center of circle in the middle of it.
        #Compare radius = max distance / 2 with radius.
        return max([a,b,c])/2 < radius
    else:
        #triangle is acute
        #calculate the circumradius of the triangle. Found formula online:
        #https://www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        r = a/(2*math.sinA)
        return r < radius

#Helper function
def euclidian_dist(p1, p2):
    return math.sqrt(pow(p1[0]-p2[0], 2) + pow(p1[1] - p2[1], 2));

def main():
    print "Hello world!"
    LIC3()
    print LIC8()
    print LIC13()


if __name__ == "__main__":
    main()
