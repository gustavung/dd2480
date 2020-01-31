# Launch Interceptor Program - DD2480 - Group 7

A launch interceptor program is a software which can decide whether an interceptor of an anti-ballistic missile system should be lanuched or not.

This software implements a launch interceptor system based on radar points and different given lanuch parameters. A launch interceptor program decides to launch an interceptor by using several Launch Interceptor Conditions (LIC) as well as different control matrices which determine how these LICs are connected.

Currently, the interceptor system use 14 different LICs constrained by user input parameters. These LICs will be used to construct a Conditions Met Vector (CMV). The CMV will be used along with the Logical Connector Matric (LCM) to determine how the LICs are contrained together. The resulting operation is stored into a Preliminary Unlocking Matrix (PUM). The software also use a Preliminary Unlocking Vector (PUV) as user input to represent which LIC actually matter in this lanuch. Finally a Final Unlocking Vector is derived from the PUV and PUM. The system will output "YES" iff all entries in the FUV is true.

The input values are stored as a json file called "global.json". They contain the following variables:
* PI - Value of pi with desired precision, eg. 3.14
* LENGTH1 - Length used in LICs 0, 7, 12
* EPSILON - Deviation from PI used in LICs 2, 9
* AREA1 - Area used in LICs 3, 10, 14
* Q_PTS - No. of consecutive points in LIC 4
* QUADS - No. of quadrants in LIC 4
* DIST - Distance used in LIC 6
* N_PTS - No. of consecutive points in LIC 6
* K_PTS - No. of consecutive points in LIC 7, 12
* A_PTS - No. of consecutive points in LIC 8, 13
* B_PTS - No. of consecutive points in LIC 8, 13
* C_PTS - No. of consecutive points in LIC 9
* D_PTS - No. of consecutive points in LIC 9
* E_PTS - No. of consecutive points in LIC 10, 14
* F_PTS - No. of consecutive points in LIC 10, 14
* G_PTS - No. of consecutive points in LIC 11
* LENGTH2 - Maximum length in LIC 12
* RADIUS2 - Maximum radius in LIC 13
* AREA2 - Maximum area in LIC 14
* NUMPOINTS - The number of data points
* POINTS - The actual data points in the format [[x1, y1], [x2, y2]] etc
* LCM - A 15x15 matrix containing the entries "ORR", "ANDD" or "Not Used"
* PUV - A boolean vector of length 15

The output will be:

* Launch decision encoded as "YES" or "NO" to the standard output
* The CMV
* The PUM
* The FUV


## Running and testing

The code can be run by using `python3 main.py`. It can be tested by running `python3 -m unittest decide_test.py lic_test.py`.

## Dependencies

This project uses the math library numpy which can be installed by the command `pip3 install -r requirements.txt` 


## Statement of contributions

* Fabian Waxin Borén - Wrote the LIC functions 4, 9, 14 with tests and set up the CIs.
* Gustav Ung - Wrote the LIC functions 1, 6, 11 with tests, drafted the README.
* Love Almgren  - Wrote the LIC functions 3, 8, 13 with tests.
* Ramiz Dündar - Wrote the LIC functions 0, 5, 10 with tests.
* Simon Zlotnik Sirén  - Wrote the LIC functions 2, 7, 12 with tests.
