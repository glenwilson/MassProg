from options import *
from r_steenrod_algebra import *
from pickle_storage import *
from wrapper import *
from E2_page import *

options = Options.default("FiniteOdd1")
myss = MASS(options)
myss.start_session()

xx = RSq(14,14,14,14,14)
xx.simplify(options)
print xx

myss.stop_session()
# xx = MASS.bit_vector.BitVector(10)
# print xx
