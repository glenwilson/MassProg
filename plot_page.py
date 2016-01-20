from E2_page import *
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

def generate_plots(E2_page, level, options):
    """
    level is an integer which corresponds to the Ext grading.
    """
    pyplot.clf()
    sheet = E2_page.get_cohomology(options)[level]
    x = []
    y = []
    bounds = options.get_degree_bounds()
    for position in sheet:
        for vector in sheet[position].get_cohomology().get_basis():
            printout = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().element_from_vector(position, vector, options)
            if E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().get_array(options)[position].get_basis():
                x.append(position[0])
                y.append(position[1])
    pair_list = []
    while x and y:
        pair_list.append((x.pop(), y.pop()))
    x = []
    y = []
    size = []
    quantity = []
    for pair in pair_list:
        x.append(pair[0])
        y.append(pair[1])
        size.append(20 + 5 * pair_list.count(pair))
        quantity.append(pair_list.count(pair))
    pyplot.scatter(x, y, s = size, c = quantity)
    pyplot.xlim([- bounds[0]-1, bounds[0]+1])
    pyplot.ylim([-bounds[1]-1, bounds[1]+1])
    pyplot.gca().invert_yaxis()
    pyplot.savefig("E2" + str(level) + "-plot")
    pyplot.close()

def my_line(x, level, bound):
    return x + level - bound

def real_plots_standard(E2_page, level, options, bounds = None):
    """
    level is an integer which corresponds to the Ext grading.
    """
    pyplot.clf()
    sheet = E2_page.get_cohomology(options)[level]
    x = []
    y = []
    if bounds == None:
        bounds = options.get_degree_bounds()
    for position in sheet:
        for vector in sheet[position].get_cohomology().get_basis():
            if E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().get_array(options)[position].get_basis():
                x.append(position[0] - level )
                y.append(position[1])
    pair_list = []
    while x and y:
        pair_list.append((x.pop(), y.pop()))
    x = []
    y = []
    size = []
    quantity = []
    for pair in pair_list:
        if pair[1] >= pair[0] + level - options.get_degree_bounds()[1]:
            x.append(pair[0])
            y.append(pair[1])
            size.append(20 + 5 * pair_list.count(pair))
            quantity.append(pair_list.count(pair))
        else:
            x.append(pair[0])
            y.append(pair[1])
            size.append(2 + 2 * pair_list.count(pair))
            quantity.append(pair_list.count(pair))
    pyplot.figure(figsize=(11,7))
    pyplot.scatter(x, y, s = size, c = quantity)
    linex = range(-bounds[0], bounds[0])
    liney = [ my_line(x, level, options.get_degree_bounds()[1]) for x in linex ]
    line2x = range(-bounds[0], bounds[0])
    line2y = [ .5*(x + level) for x in linex ]
    pyplot.plot(linex, liney, 'r', linewidth=2)
    pyplot.plot(line2x, line2y, 'r', linewidth=1)
#    pyplot.gca().set_xticks(range(- bounds[0], bounds[0], 5))
#    pyplot.gca().set_yticks(range(- bounds[0], bounds[0], 5))
#    pyplot.minorticks_on()
    pyplot.grid(True)
    pyplot.xlim([- bounds[0]-1, bounds[0]+1])
    pyplot.ylim([-bounds[1]-1, bounds[1]+1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("motivic weight")
    pyplot.title("E2 term of MASS over " + str(options.get_case()) + " with Ext grading" + str(level))
    pyplot.gca().invert_yaxis()
    pyplot.colorbar()
    if level < 10:
        pyplot.savefig(options.get_case() + "E2-" + "0" + str(level) + "-" + str(bounds[0]) + 
                       str(bounds[1]) + "-plot.png")
    else:
        pyplot.savefig(options.get_case() + "E2-" + str(level) + "-" + str(bounds[0]) + 
                       str(bounds[1]) + "-plot.png")
#    pyplot.savefig(options.get_case() + "E2-" + str(level) + "-" + str(bounds[0]) + 
#                   str(bounds[1]) + "-plot.svg")
    pyplot.close()

def complex_plots_standard(E2_page, level, options, bounds = None):
    """
    level is an integer which corresponds to the Ext grading.
    """
    pyplot.clf()
    sheet = E2_page.get_cohomology(options)[level]
    x = []
    y = []
    if bounds == None:
        bounds = options.get_degree_bounds()
    for position in sheet:
        for vector in sheet[position].get_cohomology().get_basis():
            printout = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().element_from_vector(position, vector, options)
            if E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().get_array(options)[position].get_basis():
                x.append(position[0] - level )
                y.append(position[1])
    pair_list = []
    while x and y:
        pair_list.append((x.pop(), y.pop()))
    x = []
    y = []
    size = []
    quantity = []
    for pair in pair_list:
        x.append(pair[0])
        y.append(pair[1])
        size.append(7 + 10 * pair_list.count(pair))
        quantity.append(3* pair_list.count(pair))
    pyplot.figure(figsize=(11,7))
    pyplot.scatter(x, y, s = size, c = quantity)
    line2x = range(-bounds[0], bounds[0])
    line2y = [ .5*(x + level) for x in line2x ]
    pyplot.plot(line2x, line2y, 'r', linewidth=1)
    pyplot.grid(True)
    pyplot.xlim([-1, bounds[0]+1])
    pyplot.ylim([-1 - bounds[1], bounds[1]+1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("motivic weight")
    pyplot.title("E2 term of MASS over C with Ext grading" + str(level))
    pyplot.gca().invert_yaxis()
    pyplot.savefig(options.get_case() + "E2-" + str(level) + "-" + str(bounds[0]) + 
                   str(bounds[1]) + "-plot", dpi=200)
    pyplot.close()

def complex_generator_plot(E2_page, options):
    pyplot.clf()
    x = []
    y = []
    size = []
    color = []
    bounds = options.get_degree_bounds()
    for level in range(0, len(E2_page.get_resolution().get_map_list()) ):
        sheet = E2_page.get_cohomology(options)[level]
        for position in sheet:
#            print "level " + str(level) + " position" + str(position)
            for vector in sheet[position].get_cohomology().get_basis():
                printout = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().element_from_vector(position, vector, options)
#                print printout
#this if statement rules out getting cohom from 0 dimensional vspaces
                if E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().get_array(options)[position].get_basis():
                    x.append(position[0] - level )
                    y.append(level)
                    size.append(20 + 12 * len(sheet[position].get_cohomology().get_basis() ))
                    color.append(2 + 4 * len(sheet[position].get_cohomology().get_basis() ))
    pyplot.figure(figsize=(11,7))
    pyplot.scatter(x, y, s = size, c = color)
    pyplot.grid(True)
    pyplot.xlim([-1, bounds[0]+1])
    pyplot.ylim([ -1 , bounds[0]/2 +1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("Ext grading")
    pyplot.title("E2 term of MASS over " + options.get_case() + " motivic weight supressed")
    pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                   str(bounds[1]) + "-plot", dpi=200)
    pyplot.close()


def fixed_weight_plot(E2_page, weight, options):
    logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
    pyplot.clf()
    pyplot.figure(figsize=(15,10))
    x = []
    y = []
    size = []
    color = []
    bounds = options.get_degree_bounds()
    for level in range(0, len(E2_page.get_resolution().get_map_list()) ):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[1] == weight]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    x.append(position[0] - level + counter*.2)
                    y.append(level)
                    size.append(15)
                    color.append(len(sheet[position].get_cohomology().get_basis()))
                    counter = counter + 1

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[1] == weight 
                         and xx[0] != bounds[0]]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.a1_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 1 , position[1])
                    try:
                        new_cohom = new_sheet[new_position]
                        logging.warning( "checking if product in kernel")
                        logging.warning( new_cohom.in_kernel(prod))
                        if not new_cohom.in_kernel(prod):
                            logging.warning( "A")
                            logging.warning( new_cohom.get_A())
                            logging.warning( "B")
                            logging.warning( new_cohom.get_B())
                            logging.warning("product is not in cohomology!!!")
                            #raise TypeError("product is not in cohomology!!!")
                            return
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            logging.warning( "basis for cohomology, prod was zero")
                            for thing in new_cohom.get_cohomology().get_basis():
                                logging.warning( thing)
#                            logging.warning( "matrix A")
#                            logging.warning( new_cohom.get_A())
#                            logging.warning( "matrix B")
#                            logging.warning( new_cohom.get_B())
                        else:
                            logging.warning( "product nonzero")
#                            print str(position[0] - level)
#                            print level
                            logging.warning( "matrix A")
                            logging.warning( new_cohom.get_A())
                            logging.warning( "matrix B")
                            logging.warning( new_cohom.get_B())
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .2, position[0] - level + counter_r * .2], 
                                                [level, level + 1], color='k', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.vlines(position[0]-level, level, level +.7, colors = 'r', linewidth=1)
                                logging.warning( "Undetermined line!")
                                E2_page.a1_multiple(vector, level, position, options)
                                logging.warning( "basis for cohomology")
                                for thing in new_cohom.get_cohomology().get_basis():
                                    logging.warning( thing)
                                logging.warning( "matrix A")
                                logging.warning( new_cohom.get_A())
                                logging.warning( "matrix B")
                                logging.warning( new_cohom.get_B())
                                logging.warning( "A rank")
                                logging.warning( new_cohom.get_A().get_rank())
                                logging.warning( "B nullity")
                                logging.warning( new_cohom.get_B().get_col_count() - new_cohom.get_B().get_rank())
                    except KeyError:
                        logging.warning( "key error")
                    counter_d = counter_d + 1

    pyplot.scatter(x, y, s = size, c = color)
    pyplot.grid(True)
    line2x = range(-bounds[0]/2, bounds[0] )
    line2y = [ -x + weight + bounds[0]/2 for x in line2x ]
    pyplot.plot(line2x, line2y, 'r', linewidth=1)
    pyplot.xlim([-bounds[0]/2 -1, bounds[0]+1])
    pyplot.ylim([ -1, bounds[0]/2 +1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("Ext grading")
    pyplot.title("E2 term of MASS over " + options.get_case() + " with motivic weight " + str(weight))
    if weight >= 0:
        if weight < 10:
            pyplot.savefig(options.get_case() + "E2" +  str(bounds[0]) + 
                           str(bounds[1]) + "weight" + "0" + str(weight)+".svg")
        else:
            pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                           str(bounds[1]) + "weight" + str(weight)+".png")
#        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
#                       str(bounds[1]) + "weight" + str(weight)+".svg")
    else:
        if weight > -10:
            pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                           str(bounds[1]) + "weight-n" +"0" + str(abs(weight))+".svg")
        else:
            pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                           str(bounds[1]) + "weight-n" + str(abs(weight))+".png")
#        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
#                       str(bounds[1]) + "weight-n" + str(weight)+".svg")
    pyplot.close()

def product_plot(E2_page, weight, options):
    pyplot.clf()
    pyplot.figure(figsize=(15,10))
    x = []
    y = []
    size = []
    color = []
    bounds = options.get_degree_bounds()
    for level in range(0, len(E2_page.get_resolution().get_map_list()) ):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[1] == weight]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    x.append(position[0] - level + counter*.1)
                    y.append(level)
                    size.append(15)
                    color.append(len(sheet[position].get_cohomology().get_basis()))
                    counter = counter + 1

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[1] == weight 
                         and xx[0] != bounds[0]]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.a1_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 1 , position[1])
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            print "basis for cohomology, prod was zero"
                            for thing in new_cohom.get_cohomology().get_basis():
                                print thing
                            print "matrix A"
                            print new_cohom.get_A()
                            print "matrix B"
                            print new_cohom.get_B()
                        else:
                            print "product nonzero"
                            print str(position[0] - level)
                            print level
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .1, position[0] - level + counter_r * .1], 
                                                [level, level + 1], color='k', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.vlines(position[0]-level, level, level +.7, colors = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1

    pyplot.scatter(x, y, s = size, c = color)
    pyplot.grid(True)
    line2x = range(-bounds[0]/2, bounds[0] )
    line2y = [ -x + weight + bounds[0]/2 for x in line2x ]
    pyplot.plot(line2x, line2y, 'r', linewidth=1)
    pyplot.xlim([-bounds[0]/2 -1, bounds[0]+1])
    pyplot.ylim([ -1, bounds[0]/2 +1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("Ext grading")
    pyplot.title("E2 term of MASS over " + options.get_case() + " with motivic weight " + str(weight))
    if weight >= 0:
        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                       str(bounds[1]) + "weight" + str(weight)+".png")
#        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
#                       str(bounds[1]) + "weight" + str(weight)+".svg")
    else:
        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                       str(bounds[1]) + "weight-n" + str(weight)+".png")
#        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
#                       str(bounds[1]) + "weight-n" + str(weight)+".svg")
    pyplot.close()


def isaksen_chart(E2_page, diff, options):
    """
    diff is an integer. Produces a chart where each column corresponds
    to a stable stem \pi_{n + diff, n}. We will include
    multiplications by various elements and label accordingly.
    """
    pyplot.clf()
    pyplot.figure(figsize=(15,10))
    x = []
    y = []
    size = []
    color = []
    bounds = options.get_degree_bounds()
    for level in range(0, len(E2_page.get_resolution().get_map_list()) ):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] - level - xx[1] == diff]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    x.append(position[0] - level + counter*.1)
                    y.append(level - counter * .1)
                    size.append(15)
                    color.append(len(sheet[position].get_cohomology().get_basis()))
                    counter = counter + 1

#rho multiples

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] -level - xx[1] == diff
                         and xx[0] != - bounds[0]/2 and xx[1] != -bounds[0]/2]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.p_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level]
                    new_position = (position[0] -1 , position[1] - 1)
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            pass
                        else:
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0] - level + counter_d * .1, 
                                                 position[0] - level - 1 + counter_r * .1], 
                                                [level - counter_d * .1, level - counter_r * .1 ], 
                                                color='k', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.hlines(level - counter_d * .1, position[0] - level - .7 
                                              + counter_d * .1, position[0] - level 
                                              + counter_d *.1, colors = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1

# v(0) multiples 

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] - level - xx[1] == diff 
                         and xx[0] != bounds[0]]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.v0_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 1 , position[1])
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            pass
                        else:
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .1, 
                                                 position[0] - level + counter_r * .1], 
                                                [level - counter_d *.1, level + 1 - counter_r * .1], 
                                                color='g', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.vlines(position[0]-level + counter_d * .1, 
                                              level - counter_d * .1, level - counter_d * .1 + .5, 
                                              colors = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1

# h1 multiples 

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] - level - xx[1] == diff 
                         and xx[0] <= bounds[0] - 2 and xx[1] <= bounds[1] - 1]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.h1_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 2 , position[1]+1)
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            pass
                        else:
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .1, 
                                                 position[0] - level + counter_r * .1 + 1], 
                                                [level - counter_d *.1, level + 1 - counter_r * .1], 
                                                color='m', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.plot([position[0]-level + counter_d * .1, 
                                             position[0] - level + counter_d * .1 + .5], 
                                            [level - counter_d *.1, level + .5 - counter_d * .1], 
                                            color = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1


    if not x:
        return
    pyplot.scatter(x, y)
    pyplot.grid(True)
#    line2x = range(-bounds[0]/2, bounds[0] )
#    line2y = [ -x + weight + bounds[0]/2 for x in line2x ]
#    pyplot.plot(line2x, line2y, 'r', linewidth=1)
    pyplot.xlim([-bounds[0]/2 - 1, bounds[0]+1])
    pyplot.ylim([ -1, bounds[0]/2 +1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("Ext grading")
    pyplot.title("E2 term of MASS over " + options.get_case() + " with stem - weight " + str(diff))

    if diff >= 0:
        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                       str(bounds[1]) + "diff" + str(diff)+".png")
    else:
        pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) + 
                       str(bounds[1]) + "diff-n" + str(diff)+".png")
    pyplot.close()
        
def classical_chart(E2_page, options):
    """
    diff is an integer. Produces a chart where each column corresponds
    to a stable stem \pi_{n + diff, n}. We will include
    multiplications by various elements and label accordingly.
    """
    pyplot.clf()
    pyplot.figure(figsize=(15,10))
    x = []
    y = []
    size = []
    color = []
    bounds = options.get_degree_bounds()
    for level in range(0, len(E2_page.get_resolution().get_map_list()) ):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in sheet:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    x.append(position[0] - level + counter*.1)
                    y.append(level - counter * .1)
                    size.append(15)
                    color.append(len(sheet[position].get_cohomology().get_basis()))
                    counter = counter + 1

# v(0) multiples 

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] != bounds[0]]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.v0_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 1 , position[1])
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            pass
                        else:
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .1, 
                                                 position[0] - level + counter_r * .1], 
                                                [level - counter_d *.1, level + 1 - counter_r * .1], 
                                                color='g', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.vlines(position[0]-level + counter_d * .1, 
                                              level - counter_d * .1, level - counter_d * .1 + .5, 
                                              colors = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1

# h1 multiples 

    for level in range(0, len(E2_page.get_resolution().get_map_list()) -1):
        sheet = E2_page.get_cohomology(options)[level]
        module = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain()
        for position in [xx for xx in sheet if xx[0] <= bounds[0] - 2 ]:
            if (module.get_array(options)[position].get_basis() 
                and len(sheet[position].get_cohomology().get_basis())):
                counter_d = 0
                for vector in sheet[position].get_cohomology().get_basis():
                    prod = E2_page.h1_multiple(vector, level, position, options)
                    new_sheet = E2_page.get_cohomology(options)[level + 1]
                    new_position = (position[0] + 2 , 0)
                    try:
                        new_cohom = new_sheet[new_position]
                        zero = new_cohom.get_zero_vector()
                        if new_cohom.are_cohomologous(zero, prod):
                            pass
                        else:
                            counter_r = 0
                            flag = False
                            for other_vect in new_cohom.get_cohomology().get_basis():
                                if new_cohom.are_cohomologous(other_vect, prod):
                                    pyplot.plot([position[0]-level + counter_d * .1, 
                                                 position[0] - level + counter_r * .1 + 1], 
                                                [level - counter_d *.1, level + 1 - counter_r * .1], 
                                                color='m', linewidth=1)
                                    flag = True
                                    break 
                                counter_r = counter_r + 1 
                            if not flag:
                                pyplot.plot([position[0]-level + counter_d * .1, 
                                             position[0] - level + counter_d * .1 + .5], 
                                            [level - counter_d *.1, level + .5 - counter_d * .1], 
                                            color = 'r', linewidth=1)
                    except KeyError:
                        print "key error"
                    counter_d = counter_d + 1


    if not x:
        return
    pyplot.scatter(x, y)
    pyplot.grid(True)
#    line2x = range(-bounds[0]/2, bounds[0] )
#    line2y = [ -x + weight + bounds[0]/2 for x in line2x ]
#    pyplot.plot(line2x, line2y, 'r', linewidth=1)
    pyplot.xlim([-1, bounds[0]+1])
    pyplot.ylim([ -1, bounds[0]/2 +1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("Ext grading")
    pyplot.title("E2 term of MASS over " + options.get_case())
    pyplot.savefig(options.get_case() + "E2" + str(bounds[0]) +  ".svg")
    pyplot.close()

def generator_plot(E2_page, level, options, bounds = None):
    pyplot.clf()
    sheet = E2_page.get_cohomology(options)[level]
    x = []
    y = []
    if bounds == None:
        bounds = options.get_degree_bounds()
    for position in sheet:
        for vector in sheet[position].get_cohomology().get_basis():
            printout = E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().element_from_vector(position, vector, options)
            if E2_page.get_dual_resolution(options).get_map_list()[level].get_domain().get_array(options)[position].get_basis():
                x.append(position[0] - level )
                y.append(position[1])
    pair_list = []
    while x and y:
        pair_list.append((x.pop(), y.pop()))
    x = []
    y = []
    size = []
    quantity = []
    for pair in pair_list:
        if pair[1] >= pair[0] + level - options.get_degree_bounds()[1]:
            x.append(pair[0])
            y.append(pair[1])
            size.append(20 + 5 * pair_list.count(pair))
            quantity.append(pair_list.count(pair))
        else:
            x.append(pair[0])
            y.append(pair[1])
            size.append(2 + 2 * pair_list.count(pair))
            quantity.append(pair_list.count(pair))
    pyplot.figure(figsize=(11,7))
    pyplot.scatter(x, y, s = size, c = quantity)
    linex = range(-bounds[0], bounds[0])
    liney = [ my_line(x, level, options.get_degree_bounds()[1]) for x in linex ]
    line2x = range(-bounds[0], bounds[0])
    line2y = [ .5*(x + level) for x in linex ]
    pyplot.plot(linex, liney, 'r', linewidth=2)
    pyplot.plot(line2x, line2y, 'r', linewidth=1)
#    pyplot.gca().set_xticks(range(- bounds[0], bounds[0], 5))
#    pyplot.gca().set_yticks(range(- bounds[0], bounds[0], 5))
#    pyplot.minorticks_on()
    pyplot.grid(True)
    pyplot.xlim([- bounds[0]-1, bounds[0]+1])
    pyplot.ylim([-bounds[1]-1, bounds[1]+1])
    pyplot.xlabel("topological degree - Ext grading")
    pyplot.ylabel("motivic weight")
    pyplot.title("E2 term of MASS over " + options.get_case() + " R  with Ext grading" + str(level))
    pyplot.gca().invert_yaxis()
    pyplot.savefig(options.get_case() + "E2" + str(level) + str(bounds[0]) + 
                   str(bounds[1]) + "-plot", dpi=200)
    pyplot.close()

def charts(E2_page, options):
    logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
    logging.warning("Beginning to make charts")
    if options.get_case() == "Real":
        for level in xrange(options.get_degree_bounds()[0]/2 + 1):
            real_plots_standard(E2_page, level, options)
        alist = range(-options.get_degree_bounds()[0]/2, options.get_degree_bounds()[0]/2 + 1)
        alist.reverse()
        for weight in alist:
            fixed_weight_plot(E2_page, weight, options)
    elif options.get_case() == "Complex":
        for level in xrange(options.get_degree_bounds()[0]/2 ):
            complex_plots_standard(E2_page, level, options)
        complex_generator_plot(E2_page, options)
        alist = range(-options.get_degree_bounds()[0]/2, options.get_degree_bounds()[0]/2 + 1)
        alist.reverse()
        for weight in alist:
            fixed_weight_plot(E2_page, weight, options)
    elif options.get_case() == "Classical":
        complex_generator_plot(E2_page, options)
        fixed_weight_plot(E2_page, 0, options)
    elif (options.get_case() == "FiniteOdd3"
          or options.get_case() == "FiniteOdd1"):
        for level in xrange(options.get_degree_bounds()[0]/2 + 1):
            real_plots_standard(E2_page, level, options)
        alist = range(-options.get_degree_bounds()[0]/2, options.get_degree_bounds()[0]/2 + 1)
        alist.reverse()
        for weight in alist:
            fixed_weight_plot(E2_page, weight, options)

