from r_steenrod_algebra import *
from r_polynomial import *
from r_monomial import *
from wrapper import *
from E2_page import *
import time

options = Options(
    "cx",
    PickleStorage("cx_comm_db.pickle"),
    PickleStorage("cx_adem_db.pickle"),
    "t", "p", "t*", "p*",
    { "t" : (0,1), "p" : (1,1), "u" : (1, 1), "t*" : (0, -1), 
      "p*" : (-1, -1), "u*" : (-1, -1) }, "Complex", (20, 10),
    logging.WARNING, 
    2)

myss = MASS(options)
myss.set_degree_bounds((20, 10))
myss.start_session()

res = myss.get_resolution()
myss.make_no_mat_resolution()
myss.make_dual_resolution()
myss.get_E_2_page_no_mat().compute_product_structure(myss.get_options())
#myss.get_E_2_page_no_mat().product_printout("cx_prod_printout.txt", myss.get_options())

#print myss.cohomology_info(2, (3,0))
#myss.cohomology_printout("cl_cohom_printout.txt")
#myss.make_charts()
#myss.make_charts_with_mat()
#myss.get_printout("finiteodd3.txt")
#myss.get_E_2_page_no_mat().get_dual_resolution(myss.get_options())
#myss.make_isaksen_chart()

h2 = ModElt(ModuleMonomial(RSq(), Generator("h1(4, 2)0", 
                                            (4, 2))))
h1 = ModElt(ModuleMonomial(RSq(), Generator("h1(2, 1)0", 
                                            (2, 1))))
h0 = ModElt(ModuleMonomial(RSq(), Generator("h1(1, 0)0", 
                                            (1, 0))))

massey = myss.p_operator(h1, 1)
print massey

# print myss.cohomology_info(2, (8,3))

myss.massey_product_printout("cx_massey_products.txt")

myss.stop_session()
