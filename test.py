from wrapper import *

options = Options.default("Real")
myss = MASS(options)
#myss.set_logging_level(logging.ERROR)
#myss.make_resolution()
#myss.make_no_mat_resolution()
#myss.make_dual_resolution()
myss.compute_product_structure()
#myss.make_charts()
myss.make_product_database()

myss.stop_session()
