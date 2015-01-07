from r_steenrod_algebra import *
from r_polynomial import *
from r_monomial import *
from wrapper import *
from E2_page import *
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

myss = MASS(options)
myss.set_degree_bounds((30, 15))
#res = myss.get_resolution()
#myss.make_no_mat_resolution()
#myss.make_dual_resolution()

#res.map_printout("real_map_printout.txt", myss.get_options())
#myss.get_E_2_page().compute_product_structure(myss.get_options())
#myss.get_E_2_page_no_mat().product_printout("real_prod_printout.txt", myss.get_options())
#myss.cohomology_printout("real_cohom_printout.txt")

#myss.make_charts_with_mat()
#fixed_weight_plot(myss.get_E_2_page_no_mat(), -6, myss.get_options())
#myss.get_printout("real_printout.txt")

myss.make_isaksen_chart()
