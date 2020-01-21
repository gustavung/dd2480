import json

f = open("global.json")

inp = json.load(f)

NUMPOINTS = inp["NUMPOINTS"]
POINTS = inp["POINTS"]
PARAMETERS_T = inp["PARAMETERS_T"]
LCM = inp["LCM"]
PUV = inp["PUV"]

print(NUMPOINTS, POINTS, PARAMETERS_T, LCM, PUV)
