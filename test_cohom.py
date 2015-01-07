from r_steenrod_algebra import *
from r_polynomial import *
from r_monomial import *
from wrapper import *
from E2_page import *
from bit_vector import BitVector
from bit_matrix import BitMatrix
from cohomology import *
import time

options = Options(
    PickleStorage("real_comm_db.pickle"),
    PickleStorage("real_adem_db.pickle"),
    "t", "p", "t*", "p*",
    { "t" : (0,1), "p" : (1,1), "u" : (1, 1), "t*" : (0, -1), 
      "p*" : (-1, -1), "u*" : (-1, -1) }, "Real", (20, 10),
    "real_log.log", logging.WARNING, 
    "real_resolution.pickle", 
    "real_resolution_no_mat.pickle",
    "real_dual_resolution.pickle",
    "real_a_star",
    8)

B = BitMatrix.get_blank_matrix(2,3)
B._rows[1][0]=1
B._rows[1][1]=1
B._rows[1][2]=1

A = BitMatrix.get_blank_matrix(3,6)
A._rows[0][0]=1
A._rows[1][0]=1
A._rows[1][1]=1
A._rows[2][1]=1

cohom = Cohomology(B, A)

print cohom.get_A()
print cohom.get_B()

cohom.compute_cohomology()

zero = cohom.get_zero_vector()
vect = BitVector(3)
vect[0]=1
vect[2]=1

print "and now check basis!"
print cohom.get_cohomology().get_basis()

