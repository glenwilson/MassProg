from wrapper import *

options = Options.default("FiniteOdd3")
myss = MASS(options)
#myss.set_logging_level(logging.ERROR)
myss.make_resolution()
myss.make_no_mat_resolution()
myss.make_dual_resolution()
myss.compute_product_structure()
myss.make_charts()
#myss.make_product_database()
myss.make_isaksen_chart()

myss.stop_session()
