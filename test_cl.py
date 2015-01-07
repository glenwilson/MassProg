from r_steenrod_algebra import *
from r_polynomial import *
from r_monomial import *
from wrapper import *
from E2_page import *
import time

options = Options.default("Classical")
myss = MASS(options)
myss.set_degree_bounds((28, 0))
myss.start_session()

#res = myss.get_resolution()
#res.map_printout("cl_map.txt", myss.get_options())
#myss.make_no_mat_resolution()
#myss.make_dual_resolution()
#myss.get_E_2_page_no_mat().compute_product_structure(myss.get_options())
#myss.make_product_database()

#myss.cohomology_printout("cl_cohom_printout.txt")
h2 = ModElt(ModuleMonomial(RSq(), Generator("h1(4, 0)0", 
                                            (4, 0))))
h1 = ModElt(ModuleMonomial(RSq(), Generator("h1(2, 0)0", 
                                            (2, 0))))
h0 = ModElt(ModuleMonomial(RSq(), Generator("h1(1, 0)0", 
                                            (1, 0))))

#massey = myss.p_operator(h1, 1)
#massey = myss.massey_product(h0, 1, h1, 1, h0, 1)
#print "now printing the result!"
#for thing in massey:
#    print thing

#print myss.cohomology_info(2, (12,0))
#print myss.cohomology_info(5, (20,0))

#dual_res = myss.get_E_2_page().get_dual_resolution(myss.get_options())

tests = [RSq(1,3), RSq(1,2,1), RSq(2,2) ]
for thing in tests:
    print thing
    thing.simplify(options)
    print thing

myss.stop_session()



#print myss.get_E_2_page_no_mat().get_cohomology(myss.get_options())[2].keys()


#print myss.cohomology_info(2, (3,0))
#myss.cohomology_printout("cl_cohom_printout.txt")
#myss.make_charts()
#myss.make_charts_with_mat()
#myss.get_printout("finiteodd3.txt")

#myss.get_E_2_page_no_mat().get_dual_resolution(myss.get_options())

#myss.make_classical_chart()
