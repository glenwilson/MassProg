from r_steenrod_algebra import *
from r_polynomial import *
from r_monomial import *
from wrapper import *
from E2_page import *
import time

options = Options.default("FiniteOdd1")
myss = MASS(options)
myss.set_degree_bounds((20, 10))
myss.set_numpcs(2)
myss.start_session()

res = myss.get_resolution()
#res.map_printout("fo1_map_printout.txt", myss.get_options())

#myss.make_no_mat_resolution()
#myss.make_dual_resolution()

myss.get_E_2_page_no_mat().compute_product_structure(myss.get_options())
#myss.get_E_2_page_no_mat().product_printout("fo1_prod_printout.txt", myss.get_options())

#print myss.cohomology_info(2, (3,0))
#myss.cohomology_printout("fo1_cohom_printout.txt")

#myss.make_charts_with_mat()
#myss.get_printout("fo1_gen_printout.txt")
#myss.get_E_2_page_no_mat().get_dual_resolution(myss.get_options())

#myss.make_isaksen_chart()
myss.make_product_database()
#myss.make_charts()

h2 = ModElt(ModuleMonomial(RSq(), Generator("h1(4, 2)0", 
                                            (4, 2))))
h1 = ModElt(ModuleMonomial(RSq(), Generator("h1(2, 1)0", 
                                            (2, 1))))
h0 = ModElt(ModuleMonomial(RSq(), Generator("h1(1, 0)0", 
                                            (1, 0))))

massey = myss.get_E_2_page().level_one_m_product(h0, 1, h1, 1, h0, 1, myss.get_options())
massey = myss.p_operator(h2, 1)
print "now printing the results!"
print massey

myss.massey_product_printout("fo1_massey_products.txt")

myss.stop_session()

#xx = RSq(2,4)
#xx.simplify(options)
#print xx



