from r_polynomial import *
from r_monomial import *
from r_steenrod_algebra import *
from generator import Generator
from free_A_module import * 
from module_map import * 
from cohomology import * 
from mem_storage import *
from bit_matrix import BitMatrix
from bit_vector import BitVector
from multiprocessing import *
from h_star import *
from h_dual_module import * 
import copy
import logging
import cPickle as pickle
#import matplotlib.pyplot as pyplot

class E2Page(object):
    def __init__(self, resolution, options):
        """
        resolution is a resolution object.

        dual_resolution will be computed with methods in this class. 

        cohomology is a list of dictionaries. the i'th list
        corresponds to the cohomology with ext grading i. the keys of
        the dictionary are the positions with bigrading (p,q). the
        value is a cohomology object which stores information about
        the cohomology in that location. A new addition is the product
        basis attribute of cohomology objects. a basis will be
        constructed for each cohomology object with a minimal set of
        generators. The basis element will be stored just as
        representatives in the kernel, in module element form. to get
        the product structure, use the product_dict. The keys are the
        string form of the module element, the value is a list
        [x1,...,xk] so that the key is equal to the product of the
        elements in the list. 
        
        """
        self.resolution = resolution
        self.dual_resolution = Resolution([], options)
        self.dual_resolution_flag = False
        self.cohomology = []
        self.cohomology_flag = False
        self.dual_resolution_loaded_flag = False
        self.product_dictionary = {}
        self.product_generators = []
        self.product_flag = False
        self.lol_storage = {}
        self.lol_flag = False

    def get_resolution(self):
        return self.resolution
        
    def get_dual_resolution_flag(self):
        return self.dual_resolution_flag

    def get_cohomology_flag(self):
        return self.cohomology_flag

    def get_lol_storage(self, options):
        #attempt to load pickle if lol_flag = False
        #print "the lol flag is:" + str(self.lol_flag)
        if self.lol_flag:
            return self.lol_storage
        else:
            try:
                print "Trying to load lol storage from \n" + options.get_lol_file()
                pickle_file = open(options.get_lol_file(), "rb")
                the_pickle = pickle.load(pickle_file)
                pickled_deg = the_pickle[0]
                pickled_storage = the_pickle[1]
                pickle_file.close()
                if pickled_deg == options.get_degree_bounds():
                    self.lol_storage = pickled_storage
                    print "loading success!"
                else:
                    #Here is an opportunity to extend old lol
                    #dictionary to stop duplicating work!
                    #or it can be done on the fly by checking 
                    #the list of lifts
                    self.lol_storage = {}
                    print "nothing pickled!"
            except (IOError, EOFError):
                self.lol_storage = {}
                print "loading not a success"
        self.lol_flag = True
        return self.lol_storage

    def pickle_lol_storage(self, options):
        print "trying to pickle lol storage"
        print "the pickle flag is:" + str(self.lol_flag)
        pickle_file = open(options.get_lol_file(), "wb")
        pickling = [options.get_degree_bounds(), self.lol_storage]
        pickle.dump(pickling, pickle_file, -1)
        pickle_file.close()

    def compute_dual_resolution(self, options):
        print "in compute dual resolution!!!"
        print options.get_degree_bounds()
        if not self.dual_resolution_flag:
            self.dual_resolution = Resolution([], options)
            for a_map in self.get_resolution().get_map_list():
                self.dual_resolution.get_map_list().append(make_dual_map(a_map, options))
            self.dual_resolution_flag = True

    def save_dual_resolution(self, options):
        pickle_file = open(options.get_dual_resolution_file(), "wb")
        pickle.dump(self.dual_resolution, pickle_file, -1)
        pickle_file.close()

    def load_dual_resolution(self, options):
        if not self.dual_resolution_loaded_flag:
            try:
                pickle_file = open(options.get_dual_resolution_file(), "rb")
                self.dual_resolution = pickle.load(pickle_file)
                pickle_file.close()
                first_map = self.resolution.get_map_list()[0]
                old_bounds = first_map.get_domain().get_deg_bounds()
                new_bounds = options.get_degree_bounds()
                if (len(self.dual_resolution.get_map_list()) 
                    == len(self.get_resolution().get_map_list()) 
                    and (old_bounds[0] == new_bounds[0] 
                    and old_bounds[1] == new_bounds[1])):
                    self.dual_resolution_loaded_flag = True
                else:
                    self.compute_dual_resolution(options)
            except (IOError, EOFError):
                self.compute_dual_resolution(options)

    def make_dual_resolution(self, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        dual_res = self.get_dual_resolution(options)
        for amap in dual_res.get_map_list():
            logging.warning("Computing dual at level" 
                            + str(dual_res.get_map_list().index(amap)))
            amap.multiprocess_compute_maps(options)
        self.dual_resolution = dual_res
        self.save_dual_resolution(options)

    def get_dual_resolution(self, options):
        if not self.dual_resolution_loaded_flag:
            self.load_dual_resolution(options)
        return self.dual_resolution 

#cohomology computation
            
    def compute_cohomology(self, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.warning("Computing cohomology")
        temp = (ModuleMonomial(RSq(), Generator("temp", (0,0))))
        zero_domain = FreeHDualModule([ModElt(temp)], 
                                      options.get_degree_bounds())
        zero_codomain = self.get_dual_resolution(
            options).get_map_list()[0].get_domain()
        zero_map_dict = {}
        output = ModElt()
        output.scalar_multiply(RPolynomial(()), options)
        zero_map_dict[temp.get_generator().get_name()] = output
        zero_map = FreeHDualModuleMap(zero_domain, 
                                      zero_codomain, zero_map_dict)
        for index in range(0, len(self.get_resolution().get_map_list())):
            current_map = self.get_dual_resolution(
                options).get_map_list()[index]
            if index == 0:
                previous_map = zero_map
            else:
                previous_map = self.get_dual_resolution(
                    options).get_map_list()[index - 1]
            new_array = {}
            for position in [ pair for pair in current_map.get_domain().get_array(options) if pair[1] >=  pair[0] - options.get_degree_bounds()[0]/2]:
                new_array[position] = Cohomology(
                    current_map.get_map_at(position, options), 
                    previous_map.get_map_at(position, options))
            self.cohomology.append(new_array)
        self.cohomology_flag = True

    def multiprocess_compute_cohomology(self, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        numpcs = options.get_numpcs()
        logging.warning("Computing cohomology")
        temp = (ModuleMonomial(RSq(), Generator("temp", (0,0))))
        zero_domain = FreeHDualModule([ModElt(temp)], 
                                      options.get_degree_bounds())
        zero_codomain = self.get_dual_resolution(
            options).get_map_list()[0].get_domain()
        zero_map_dict = {}
        output = ModElt()
        output.scalar_multiply(RPolynomial(()), options)
        zero_map_dict[temp.get_generator().get_name()] = output
        zero_map = FreeHDualModuleMap(zero_domain, 
                                      zero_codomain, zero_map_dict)
        for index in range(0, len(self.get_resolution().get_map_list())):
            current_map = self.get_dual_resolution(
                options).get_map_list()[index]
            if index == 0:
                previous_map = zero_map
            else:
                previous_map = self.get_dual_resolution(
                    options).get_map_list()[index - 1]
            new_array = {}
            if options.get_case() == "Classical":
                inputs = [ pair for pair in current_map.get_domain().get_array(options) ]
            else:
                inputs = [ pair for pair in current_map.get_domain().get_array(options) if pair[1] >= pair[0] - options.get_degree_bounds()[0]/2]
            out_q = Queue()
            chunksize = len(inputs)/numpcs
            procs = []
            for i in range(numpcs + 1):
                p = Process(
                    target=cohomology_worker,
                    args=(current_map, previous_map, 
                          inputs[chunksize * i : chunksize * (i + 1)], 
                          options, out_q))
                procs.append(p)
                p.start()
            resultdict = {}
            for i in range(numpcs + 1):
                resultdict.update(out_q.get())

            for p in procs:
                p.join()
            for key in resultdict.keys():
                output = resultdict[key]
                new_array[output[0]] = output[1]
            self.cohomology.append(new_array)
        self.cohomology_flag = True

    def get_cohomology(self, options):
        if not self.get_cohomology_flag():
            self.multiprocess_compute_cohomology(options)
        return self.cohomology

    def get_cohomology_dimension(self, level, position, options):
        sheet = self.get_cohomology(options)[level]
        module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        dim = len(sheet[position].get_cohomology().get_basis())
        if not module.get_array(options)[position].get_basis():
            return 0
        else:
            return dim

    def vector_from_element(self, element, level, options):
        position = element.get_degree(options)
        module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        return module.vector_from_element(element, position, options)

    def element_from_vector(self, vector, level, position, options):
        module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        return module.element_from_vector(position, vector, options)

    def get_cohomologous_elements(self, element, level, options):
        position = element.get_degree(options)
        sheet = self.get_cohomology(options)[level]
        cohom = sheet[position]
        vector = self.vector_from_element(element, level, options)
        coset_vectors = cohom.coset(vector)
        coset_elt = set()
        for coset_vect in coset_vectors:
            coset_elt.add(self.element_from_vector(
                coset_vect, level, position, options))
        return coset_elt
        
    def short_representative(self, element, level, options):
        module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        position = element.get_degree(options)
        sheet = self.get_cohomology(options)[level]
        cohom = sheet[position]
        vector = self.vector_from_element(element, level, options)
        rep_vector = cohom.short_representative(vector)
        return self.element_from_vector(rep_vector, level, position, options)

    def zero_in_cohomology(self, element, level, options):
        sheet = self.get_cohomology(options)[level]
        position = element.get_degree(options)
        cohom = sheet[position]
        zero = cohom.get_zero_vector()
        vector = self.vector_from_element(element, level, options)
        if cohom.are_cohomologous(zero, vector):
            return True
        else:
            return False

#Product structure

    def initial_lift_dual_map(self, module, dual_elt, options):
        """
        dual_elt is in the dual of module. 
        """
        domain = module
        codomain = self.get_resolution().get_map_list()[0].get_codomain()
        bounds = codomain.get_deg_bounds()
        iota = codomain.get_generator_list()[0]
        generator_map = {}
        for thing in domain.get_generator_list():
            generator_map[thing.get_summands()[0].get_generator().get_name()] \
                = ModElt()
        dual_elt.canonical_form(options)
        dual_elt.combine_monomials(options)
        for summand in dual_elt.get_summands():
            coefficient = summand.get_coefficient().copy()
            coefficient.make_standard(options)
            image= iota.copy()
            image.scalar_multiply(coefficient, options)
            if (image.get_degree(options)[0] <= bounds[0] 
                and image.get_degree(options)[1] <= bounds[1]):
                generator_map[summand.get_generator().get_name()] = image
        return FreeAModuleMap(domain, codomain, generator_map)

    def compute_list_of_lifts(self, index, dual_elt, length, options):
        """
        index describes the codomain of the map at position index in
        the resolution.  

        dual_elt is in the dual of the above module
        length + index needs to be less than length of resolution

        currently disregards desired length and just computes all lifts
        which are possible

        what is the ordering for the elements in lol?
        would like lol[j] to be the map F_j --> F_(j- index)
        """
        max_length = options.get_degree_bounds()[0]/2 - index
        lift_list = []
        initial_lift = self.initial_lift_dual_map(
            self.get_resolution().get_map_list()[index].get_codomain(), 
            dual_elt, options)
        lift_list.append(initial_lift)
        for i in xrange(max_length):
            _map = lift_list[i]
            top_res_map = self.get_resolution().get_map_list()[index + i]
            bottom_res_map = self.get_resolution().get_map_list()[i]
            new_domain = top_res_map.get_domain()
            bounds = options.get_degree_bounds()
            new_codomain = bottom_res_map.get_domain()
            new_dict = {}
            comp_map = _map.compose(top_res_map, options)
            for generator in new_domain.get_generator_list():
                output = comp_map.evaluate(generator, options)
                position = (generator.get_degree(options)[0] 
                            - dual_elt.get_degree(options)[0], 
                            generator.get_degree(options)[1] 
                            - dual_elt.get_degree(options)[1])
                if not position in _map.get_codomain().get_array(options):
                    out_vector = BitVector(1)
                    send_to = ModElt()
                    new_dict[generator.get_summands()[0].get_generator().get_name()] = send_to
                else:
                    out_vector = _map.get_codomain().vector_from_element(output, position, options)
                    lifted_vector = bottom_res_map.get_map_at(position, options).solve(out_vector)
                    send_to = new_codomain.element_from_vector(position, lifted_vector, options)
                    new_dict[generator.get_summands()[0].get_generator().get_name()] = send_to
                
            new_lift = FreeAModuleMap(new_domain, new_codomain, new_dict)
            lift_list.append(new_lift)
        dual_elt.canonical_form(options)
        self.lol_storage[str(dual_elt)] = lift_list

    def get_list_of_lifts(self, index, dual_elt, length, options):
        """
        index describes the codomain of the map at position index in
        the resolution.  
        dual_elt is in the dual of the above module
        length + index needs to be less than length of resolution
        """
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.debug("lol storage keys")
        for thing in self.get_lol_storage(options):
            logging.debug(str(thing))
        dual_elt.canonical_form(options)
        logging.debug("desired key " + str(dual_elt))
        try:
            lol = self.get_lol_storage(options)[str(dual_elt)]
            if len(lol) < length + 1:
                logging.warning("had to recompute list of lifts")
                self.compute_list_of_lifts(index, dual_elt, length, options)
            return self.get_lol_storage(options)[str(dual_elt)]
        except KeyError:
            logging.warning("there was a key error with lol storage")
            self.compute_list_of_lifts(index, dual_elt, length, options)
            return self.get_lol_storage(options)[str(dual_elt)]

    def compute_product(self, mod_elt1, mod_elt2, pos1, pos2, options):
        """ this returns a map which upon killing squares gives, in
        map form, the product of gen1 * gen2
        mod_elt1 is in pos1 in the filtration
        mod_elt2 is in pos2 in the filtration
        """
        lift_list = self.get_list_of_lifts(pos1, mod_elt1, pos2, options)
        gen2_map = self.initial_lift_dual_map(
            self.get_resolution().get_map_list()[pos2].get_codomain() , 
            mod_elt2, 
            options)
        output = gen2_map.compose( lift_list[pos2] , options)
        output.kill_squares(options)
        element = ModElt()
        for generator in output.get_domain().get_generator_list():
            result = output.evaluate(generator, options)
            result.combine_monomials(options)
#            print "result of evaluating on gen"
#            print result
            if result.get_summands():
                coefficient = result.get_summands()[0].get_coefficient().copy()
                coefficient.make_dual(options)
                dual_summand = ModElt(ModuleMonomial(
                            coefficient, generator.get_summands()[0].get_generator()))
                element.add(dual_summand)
#                print "the updated element"
#                print element
        return element

    def compute_product_structure(self, options):
        if self.product_flag:
            return
        for index in xrange(len(self.get_cohomology(options))):
            self.generate_product_structure(index, options)
        self.product_flag = True
#        self.pickle_lol_storage(options)

    def generate_product_structure(self, level, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        sheet = self.get_cohomology(options)[level]
        module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        pos = sheet.keys()[:]
        pos.sort()
        pos.reverse()
        logging.warning( "AT LEVEL" + str(level))
        for pair in pos:
            logging.debug( str(pair))
            cohomology = sheet[pair]
            if level > 0:
                prev_module = self.get_dual_resolution(options).get_map_list()[level - 1].get_domain()
                prev_map = self.get_dual_resolution(options).get_map_list()[level -1 ]
            if not self.get_cohomology_dimension(level, pair, options):
                #this ensures that the 0 dim'l cohomology follows convention
                cohomology.add_to_product_basis(cohomology.get_cohomology().get_basis())
            else:
                if (len(cohomology.get_product().get_basis()) 
                    < self.get_cohomology_dimension(level, pair, options)):
                    #check what was missed, and add it
                    #this is currently missing some rho multiples!!! 
                    for vect in cohomology.get_cohomology().get_basis():
                        if not cohomology.in_cohomology_subspace(
                            cohomology.get_product().get_basis(), 
                            vect):
                            cohomology.add_to_product_basis([vect])
                            new_elt=module.element_from_vector(
                                    pair, 
                                    vect, 
                                    options)
                            logging.debug("new_elt to add")
                            logging.debug(str( new_elt))
                            self.product_generators.append(new_elt)
                            self.update_products(new_elt, level, options)
                    logging.debug( "new dimensions!")
                    logging.debug(str( len(cohomology.get_product().get_basis())))
                    logging.debug(str( self.get_cohomology_dimension(level, pair, options)))
        logging.warning( "the generators")
        for thing in self.product_generators:
            logging.warning(str(thing))

    def a1_multiple(self, vector, level, position,  options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        a1 = ModElt(ModuleMonomial(RSq(), Generator("h1(1, 0)0", (1, 0))), ModuleMonomial(RSq("p*"), Generator("h1(2, 1)0", (2, 1))) )
        other_module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        element = other_module.element_from_vector(position, vector, options)
        product = self.compute_product(a1, element, 1, level, options)
        new_level = level + 1
        new_module = self.get_dual_resolution(
            options).get_map_list()[new_level].get_domain()
        new_pos = (position[0] + 1, position[1])
        new_vect = new_module.vector_from_element(product, new_pos, options)
        logging.debug("a1 " + str(a1))
        logging.debug("element " + str(element))
        logging.debug("product " + str(product))
        logging.debug("new_vect " + str(new_vect))
        return new_vect

    def v0_multiple(self, vector, level, position,  options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        v0 = ModElt(ModuleMonomial(RSq(), Generator("h1(1, 0)0", (1, 0))))
        other_module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        element = other_module.element_from_vector(position, vector, options)
        product = self.compute_product(v0, element, 1, level, options)
        new_level = level + 1
        new_module = self.get_dual_resolution(
            options).get_map_list()[new_level].get_domain()
        new_pos = (position[0] + 1, position[1])
        new_vect = new_module.vector_from_element(product, new_pos, options)
        logging.debug("v0 " + str(v0))
        logging.debug("element " + str(element))
        logging.debug("product " + str(product))
        logging.debug("new_vect " + str(new_vect))
        return new_vect

    def h1_multiple(self, vector, level, position,  options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        h1 = ModElt(ModuleMonomial(RSq(), Generator("h1(2, 1)0", (2, 1))))
        if options.get_case() == "Classical":
            h1 = ModElt(ModuleMonomial(RSq(), Generator("h1(2, 0)0", (2, 0))))
        other_module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        element = other_module.element_from_vector(position, vector, options)
        product = self.compute_product(h1, element, 1, level, options)
        new_level = level + 1
        new_module = self.get_dual_resolution(
            options).get_map_list()[new_level].get_domain()
        new_pos = (position[0] + 2, position[1] + 1)
        if options.get_case() == "Classical":
            new_pos = (position[0] + 2 , 0)
        new_vect = new_module.vector_from_element(product, new_pos, options)
        logging.debug("h1 " + str(h1))
        logging.debug("element " + str(element))
        logging.debug("product " + str(product))
        logging.debug("new_vect " + str(new_vect))
        return new_vect

    def p_multiple(self, vector, level, position, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        p = ModElt(ModuleMonomial(RSq("p*"), Generator("i", (0,0))))
        if options.get_case() == "FiniteOdd1":
            p = ModElt(ModuleMonomial(RSq("u*"), Generator("i", (0,0))))
        other_module = self.get_dual_resolution(options).get_map_list()[level].get_domain()
        element = other_module.element_from_vector(position, vector, options)
        product = self.compute_product(p, element, 0, level, options)
        new_level = level
        new_module = other_module
        new_pos = (position[0] - 1, position[1] - 1)
        new_vect = new_module.vector_from_element(product, new_pos, options)
        logging.debug("elt " + str(p))
        logging.debug("element " + str(element))
        logging.debug("product " + str(product))
        logging.debug("new_vect " + str(new_vect))
        return new_vect

    def update_products(self, element, level, options):
        """
        element is in the ext grading level
        """
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.warning( "deg of elt " + str(element.get_degree(options)))
        if level == 0 and element.get_degree(options) == (0,0):
            return
        bounds = options.get_degree_bounds()
        for counter in range(0, len(self.get_cohomology(options)) - level):
            sheet = self.get_cohomology(options)[counter]
            module = self.get_dual_resolution(
                options).get_map_list()[level].get_domain()
            other_module = self.get_dual_resolution(options).get_map_list()[counter].get_domain()
            pos = sheet.keys()[:]
            pos.sort()
            pos.reverse()
            for pair in pos:
                logging.debug( "at position " + str(pair))
                logging.debug( "counter " + str(counter))
                cohomology = sheet[pair]
                if counter == 0 and pair == (0, 0):
                    "should skip!!!"
                    pass
                elif not (-bounds[0] <= element.get_degree(options)[0] + pair[0] and element.get_degree(options)[0] + pair[0] <= bounds[0] and -bounds[1] <= element.get_degree(options)[1] + pair[1] and element.get_degree(options)[1] + pair[1] <= bounds[1]):
                    pass
                #this should be the product dimension??? does it matter???
                elif self.get_cohomology_dimension(counter, pair, options):
                    logging.debug( "cohom dimension " + str(self.get_cohomology_dimension(counter, pair, options)))
                    for vect in cohomology.get_product().get_basis():
                        logging.debug( "the vector " + str(vect))
                        logging.debug( "cohom dim " + str(self.get_cohomology_dimension(counter, pair, options)))
                        thing = other_module.element_from_vector(
                            pair, vect, options)
                        product = self.compute_product(
                            element, thing, level, counter, options)
                        new_level = counter + level
                        new_sheet = self.get_cohomology(options)[new_level]
                        new_keys = new_sheet.keys()
                        logging.debug( "new level " + str(new_level))
                        new_pos = (element.get_degree(options)[0] + thing.get_degree(options)[0], element.get_degree(options)[1] + thing.get_degree(options)[1])
                        logging.debug( "new pos " + str(new_pos))
                        new_module = self.get_dual_resolution(
                            options).get_map_list()[new_level].get_domain()
                        if new_module.get_array(options)[new_pos].get_basis() and new_pos in new_keys:
                            new_cohom = self.get_cohomology(options)[new_level][new_pos]
                            new_vect = new_module.vector_from_element(product, new_pos, options)
                            logging.debug( "multiplying " + str(element) + " and " + str(thing))
                            logging.debug( "the product " + str(product))
                            logging.debug( "the product vector " + str(new_vect))
                            # for thing in  new_module.generator_list:
                            #     print thing
                            # print "the stuff in new module at new_pos"
                            # for thing in new_module.get_array(options)[new_pos].get_basis():
                            #     print thing
                            if new_cohom.in_cohomology_subspace(new_cohom.get_product().get_basis(), new_vect):
                                logging.debug( "not a new product")
                                if str(product) in self.product_dictionary:
                                    self.product_dictionary[str(product)].append((element, thing))
                                else:
                                    self.product_dictionary[str(product)] = [(element, thing)]
                            else:
                                logging.debug("added new basis elt")
                                new_cohom.add_to_product_basis([new_vect])
                                if str(product) in self.product_dictionary:
                                    self.product_dictionary[str(product)].append((element, thing))
                                else:
                                    self.product_dictionary[str(product)] = [(element, thing)]

    def product_description(self, element, options):
        """This only works for product basis elements right now. In general,
        need to write out in terms of product basis, and then use
        description for the basis elements.

        """
        self.compute_product_structure(options)
        factorizations = {} 
        if not str(element) in self.product_dictionary:
            return [element, ]
        else:
            stack = []
            stack.append( (element, self.product_dictionary[str(element)][:], []) )
            while stack:
                entry = stack[-1]
                if entry[1]:
                    for pair in entry[1]:
                        if str(pair[1]) in factorizations:
                            for f_list in factorizations[str(pair[1])]:
                                new_list = f_list[:]
                                entry[2].append(new_list.append(pair[0]))
                            entry[1].remove(pair)
                        elif str(pair[1]) in self.product_dictionary:
                            stack.append((pair[1],\
                                self.product_dictionary[str(pair[1])][:],\
                            []) )
                        else:
                            factorizations[str(pair[1])] \
                                = [[pair[1]]]
                            entry[1].remove(pair)
                            entry[2].append([pair[0], pair[1]])
                else:
                    factorizations[str(entry[0])] = entry[2]
                    stack.pop()
        return factorizations[str(element)]


    def product_description_string(self, element, options):
        """This only works for product basis elements right now. In general,
        need to write out in terms of product basis, and then use
        description for the basis elements.

        """
        self.compute_product_structure(options)
        factorizations = {} 
        if not str(element) in self.product_dictionary:
            return [element, ]
        else:
            stack = []
            stack.append( (element, self.product_dictionary[str(element)][:], []) )
            while stack:
                entry = stack[-1]
                if entry[1]:
                    for pair in entry[1]:
                        if str(pair[1]) in factorizations:
                            for string in factorizations[str(pair[1])]:
                                entry[2].append(str(pair[0]) + " . " + string)
                            entry[1].remove(pair)
                        elif str(pair[1]) in self.product_dictionary:
                            stack.append((pair[1],\
                                self.product_dictionary[str(pair[1])][:],\
                                []) )
                        else:
                            factorizations[str(pair[1])] \
                                = [str(pair[1])]
                            entry[1].remove(pair)
                            entry[2].append(str(pair[0]) + " . " +str(pair[1]))
                else:
                    factorizations[str(entry[0])] = entry[2]
                    stack.pop()
        return factorizations[str(element)]

    # Massey products for bar resolution
    # This does not work!!! Need to use cobar resolution...
    # Minimal resolution is not a DG algebra

    def specific_m_product(self, uu, level_uu, vv, level_vv, 
                           ww, level_ww, aa, bb, options):
        #will assume uu*vv = 0 and vv*ww = 0
        #be sure it is true before passing in! 
        aaww = self.compute_product(aa, ww, level_uu + level_vv + \
                                    -1, level_ww, options)
        uubb = self.compute_product(uu, bb, level_uu, 
                               level_vv + level_ww -1, options)
        print "aaww"
        print aaww
        print "uubb"
        print uubb
        out = aaww + uubb
        out.canonical_form(options)
        return out

    def m_preimage(self, uu, level_uu, vv, level_vv, out_style ,options):
        """
        Takes uu, vv, 
        Checks if uu*vv = 0, should this fail, returns False
        (or should it raise an exception?)
        If so, determines the set of all solutions to d(a) = uu*vv

        out_style is to be either "single_element" or "set_element"
        "single_vector" or "set_vector".

        depending on whether you want a single preimage as output, 
        or the full set of preimages, either as elements or vectors
        """
        print "finding preimage"
        product = self.compute_product(uu, vv, level_uu, 
                                       level_vv, options)
        print "the product"
        print product
        print "the level"
        print level_uu + level_vv
        sheet = self.get_cohomology(options)[level_uu + level_vv]
        uu_deg = uu.get_degree(options)
        vv_deg = vv.get_degree(options)
        position = vector_addition(uu_deg, vv_deg)
        print position
        cohom = sheet[position]
        zero = cohom.get_zero_vector()
        product_vector = self.vector_from_element(product, level_uu + level_vv, options)
        print "the product vector"
        print product_vector
        print "the matrices involved"
        print cohom.get_A()
        print cohom.get_B()
        if not cohom.are_cohomologous(zero, product_vector):
            return False
        if out_style == "set_vector":
            vect_preimages = cohom.get_A().all_solutions(
                product_vector)
            return vect_preimages
        elif out_style == "single_vector":
            pre_vect = cohom.get_A().solve(product_vector)
            return pre_vect
        elif out_style == "set_element":
            vect_preimages = cohom.get_A().all_solutions(
                product_vector)
            elt_preimages = set()
            for pre_vect in vect_preimages:
                elt_preimages.add(self.element_from_vector(pre_vect, level_uu + level_vv -1, position, options))
            return elt_preimages
        elif out_style == "single_element":
            pre_vect = cohom.get_A().solve(product_vector)
            pre_element = self.element_from_vector(pre_vect, level_uu + level_vv -1, position, options)
            return pre_element
    
    def single_massey_product(self, uu, level_uu, vv, level_vv, ww, 
                              level_ww, options):
        aa = self.m_preimage(uu, level_uu, vv, level_vv, 
                             "single_element", options)
        bb = self.m_preimage(vv, level_vv, ww, level_ww, 
                             "single_element", options)
        m_p = self.specific_m_product(uu, level_uu, vv, level_vv, 
                           ww, level_ww, aa, bb, options)
        print "the aa"
        print aa
        print "the bb"
        print bb
        print "the uu"
        print uu
        print "the vv"
        print vv
        print "the ww"
        print ww
        return m_p

    def massey_product(self, uu, level_uu, vv, level_vv, ww, 
                       level_ww, options):
        aa_set = self.m_preimage(uu, level_uu, vv, level_vv, 
                             "set_element", options)
        bb_set = self.m_preimage(vv, level_vv, ww, level_ww, 
                             "set_element", options)
        out_set = set()
        for pair in set((x,y) for x in aa_set for y in bb_set):
            print "the aa rep"
            print pair[0]
            print "the bb rep"
            print pair[1]
            print "uu"
            print uu
            print "vv"
            print vv
            print "ww"
            print ww
            out_set.add(self.specific_m_product(uu, level_uu, vv, \
                    level_vv, ww, level_ww, pair[0], pair[1], options))
        return out_set
            
    # This is overkill. Don't need to go through all reps of u,v,w. 
    #
    # def total_massey_product(self, uu, level_uu, vv, level_vv, ww, 
    #                    level_ww, options):
    #     uu_set = self.get_cohomologous_elements(uu, level_uu, 
    #                                             options)
    #     vv_set = self.get_cohomologous_elements(vv, level_vv,
    #                                             options)
    #     ww_set = self.get_cohomologous_elements(ww, level_ww, 
    #                                             options) 
    #     out_set = set()
    #     for triple in set((u,v,w) for u in uu_set for v in vv_set \
    #                       for w in ww_set):
    #         print "the representatives"
    #         print triple[0]
    #         print triple[1]
    #         print triple[2]
    #         out_set.update(self.massey_product(triple[0], level_uu, 
    #                                           triple[1], level_vv, 
    #                                           triple[2], level_ww, 
    #                                           options))
    #     return out_set
        

    # Specific massey product < h_i, x, y >
    # this doesn't work for the motivic cases! 

    def level_one_m_product(self, hh, level_hh, xx, level_xx, yy, level_yy, options):
        """
        hh is assumed to be of the form 1.h1(2^i, 2^{i-1})0

        xx and yy also assumed to be 1.hj(a,b)s
        """
        #check products, if they are non-zero, return false
        hhxx = self.compute_product(hh, xx, level_hh, 
                                       level_xx, options)
        xxyy = self.compute_product(xx, yy, level_xx, 
                                    level_yy, options)
        if not (self.zero_in_cohomology(hhxx, level_hh + level_xx, 
                                        options) and \
                self.zero_in_cohomology(xxyy, level_xx + level_yy, 
                                        options)):
            return False
        hh_deg = hh.get_degree(options)
        xx_deg = xx.get_degree(options)
        yy_deg = yy.get_degree(options)
        output = ModElt()
        coefficients = h_star(options.get_degree_bounds()[0], options.get_degree_bounds()[1], options) 
        #get the list of lifts for yy
        lol = self.get_list_of_lifts(level_yy, yy, level_xx, options)  
        _map = lol[level_xx] #or level_yy + level_xx

        for pair in [(x,y) for x in coefficients.keys() \
                     if vector_addition(hh_deg, xx_deg, yy_deg, x)
                     in _map.get_domain().get_array(options).keys()
                     for y in coefficients[x]]:
            coeff = pair[1]
            coeff_deg = pair[0]
            position = vector_addition(hh_deg, xx_deg, yy_deg, coeff_deg)
            domain_basis = _map.get_domain().get_array(options)[position].get_basis()
            if not domain_basis:
                raise TypeError("doesn't seem to be any elements in this position")
            search_elt = xx.copy()
            search_elt.scalar_multiply(RSq(hh.get_degree(options)[0]), options)
            search_elt.scalar_multiply(coeff, options)
            search_mon = search_elt.get_summands()[0]

            #look for those G such that yy(G) contains Sq^{2^i}.xx
            #add such G together to get an element in the Massey product
            for element in domain_basis:
                image = _map.evaluate(element, options)
                for summand in image.get_summands():
                    if summand.is_equal_to(search_mon):
                        element_copy = element.copy()
                        element_copy.scalar_multiply(coeff, options)
                        element_copy.make_dual(options)
                        if element_copy.get_degree(options) == vector_addition(hh_deg, xx_deg, yy_deg):
                            output.add(element_copy)
        output.kill_squares(options)
        output.canonical_form(options)
        short_out = self.short_representative(output, level_xx + level_yy, options)
        return short_out


    # def get_m_product(self, hh, level_hh, xx, level_xx, yy, level_yy, options):
    #     """
    #     hh is assumed to be of the form 1.h1(2^i, 2^{i-1})0

    #     xx and yy also assumed to be 1.hj(a,b)s
    #     """
    #     #check products, if they are non-zero, return false
    #     hhxx = self.compute_product(hh, xx, level_hh, 
    #                                    level_xx, options)
    #     xxyy = self.compute_product(xx, yy, level_xx, 
    #                                 level_yy, options)
    #     if not (self.zero_in_cohomology(hhxx, level_hh + level_xx, 
    #                                     options) and \
    #             self.zero_in_cohomology(xxyy, level_xx + level_yy, 
    #                                     options)):
    #         return False
    #     hh_deg = hh.get_degree(options)
    #     xx_deg = xx.get_degree(options)
    #     yy_deg = yy.get_degree(options)
    #     position = vector_addition(hh_deg, xx_deg, yy_deg)

    #     #get the list of lifts for yy
    #     yy_lol = self.get_list_of_lifts(level_yy, yy, level_xx, options)
    #     yy_map = yy_lol[level_xx] #or level_yy + level_xx
    #     domain_basis = _map.get_domain().get_array(options)[position].get_basis()
    #     if not domain_basis:
    #         raise TypeError("doesn't seem to be any elements in this position")

    #     xx_lol = self.get_list_of_lifts(level_xx, xx, 1, options)
    #     xx_map = xx_lol[0] 

    #     xxyy = xx_map.compose(yy_map, options)

    #     cohomology = self.get_cohomology(options)[level_xx + level_yy][

    #     #compute xx_map and yy_map
    #     #construct the chain homotopy h_1 lifting xx_map \circ yy_map
    #     #compose a \circ h_1
    #     #evaluate this map on basis elements to determine the dual class

    #     output = ModElt()
    #     search_elt = xx.copy()
    #     search_elt.scalar_multiply(RSq(hh.get_degree(options)[0]), options)
    #     search_mon = search_elt.get_summands()[0]
    #     #look for those G such that yy(G) contains Sq^{2^i}.xx
    #     #add such G together to get an element in the Massey product
    #     print "the search monomial " + str(search_mon)
    #     print "this is the domain basis"
    #     for element in domain_basis:
    #         print element
    #     for element in domain_basis:
    #         print "the element " + str(element)
    #         image = _map.evaluate(element, options)
    #         print "the image " + str(image)
    #         for summand in image.get_summands():
    #             if summand.is_equal_to(search_mon):
    #                 output.add(element)
    #     return output
    #     #another function can calculate the indeterminacy to see if
    #     #this computes the entire Massey product

                               
#Information about E2 page


    def printout(self, filename, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.warning("Beginning to compute cohomology for printout")
        printout_string = ""
        for z_index in range(0, len(self.get_cohomology(options))):
            logging.warning("at level " + str(z_index) + " for printout")
            z_level = self.get_cohomology(options)[z_index]
            printout_string = printout_string + "\nLevel" + str(z_index)
            pair_list = z_level.keys()
            pair_list.sort()
            pair_list.reverse()
            for position in pair_list:
                printout_string = printout_string + "\nE2 " + str(z_index) + str(position)
                for thing in z_level[position].get_cohomology().get_basis():
                    printout_string = printout_string + "\n" + str(self.get_dual_resolution(options).get_map_list()[z_index].get_domain().element_from_vector(position, thing, options))
        out_file = open(filename, "w+")
        out_file.write(printout_string)
        out_file.close()

    def product_printout(self, filename, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.warning("Beginning to compute cohomology for printout")
        printout_string = ""
        for z_index in range(0, len(self.get_cohomology(options))):
            logging.warning("at level " + str(z_index) + " for printout")
            z_level = self.get_cohomology(options)[z_index]
            printout_string = printout_string + "\nLevel" + str(z_index)
            pair_list = z_level.keys()
            pair_list.sort()
            pair_list.reverse()
            for position in pair_list:
                printout_string = printout_string + "\nE2 " + str(z_index) + str(position)
                for thing in z_level[position].get_product().get_basis():
                    elt = self.get_dual_resolution(options).get_map_list()[z_index].get_domain().element_from_vector(position, thing, options)
                    printout_string = printout_string + "\n" \
                        + str(elt) \
                        + " = " \
                        + str(self.product_description_string(elt, options))
        out_file = open(filename, "w+")
        out_file.write(printout_string)
        out_file.close()


#Misc functions needed by E2_page
#Should make some static methods?

def cohomology_worker(current_map, previous_map, positions, options, out_q):
    out_dict = {}
    for position in positions:
        cohom = Cohomology(
            current_map.get_map_at(position, options),
            previous_map.get_map_at(position, options))

        cohom.compute_cohomology()
        out_dict[position] = (position, cohom)
    out_q.put(out_dict)

def make_dual_map(a_map, options):
    logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
    logging.warning("Making a dual map")
    if options.get_case() == "Real":
        return make_real_dual_map(a_map, options)
    elif options.get_case() == "Complex":
        return make_complex_dual_map(a_map, options)
    elif options.get_case() == "Classical":
        return make_complex_dual_map(a_map, options)
    elif options.get_case() == "FiniteOdd3":
        return make_real_dual_map(a_map, options)
    elif options.get_case() == "FiniteOdd1":
        return make_real_dual_map(a_map, options)
    else:
        raise TypeError("Unknown case")

def make_real_dual_map(a_map, options):
    dual_map_dict = {}
    dual_map_domain_list = []
    dual_map_codomain_list = [] 

    for generator in a_map.get_codomain().get_generator_list():
            dual_map_domain_list.append(generator)

    for generator in a_map.get_domain().get_generator_list():
            dual_map_codomain_list.append(generator)
    
    for generator in dual_map_domain_list:
        value = ModElt()
        for target in a_map.get_domain().get_generator_list():
            # if ((target.get_degree(options)[0] <= 
            #      2* (generator.get_degree(options)[0] 
            #          - generator.get_degree(options)[1])
            #      and target.get_degree(options)[0] >= 
            #      generator.get_degree(options)[0])):
            if True:
                output = a_map.evaluate(target, options)
                coefficient = output.get_generator_coefficient(
                    generator.get_summands()[0].get_generator(), options)
                dual_coefficient = coefficient.get_dual(options)
                target_copy = target.copy()
                target_copy.scalar_multiply(dual_coefficient, options)
                value.add(target_copy)
        value.canonical_form(options)
        dual_map_dict[generator.get_summands()[0].get_generator().get_name()] = value
                        
    return FreeHDualModuleMap(
        FreeHDualModule(dual_map_domain_list,
                        options.get_degree_bounds()), 
        FreeHDualModule(dual_map_codomain_list,
                        options.get_degree_bounds()),
        dual_map_dict)
        
def make_complex_dual_map(a_map, options):
    dual_map_dict = {}
    dual_map_domain_list = []
    dual_map_codomain_list = [] 
    a_map.kill_squares(options)
    
    for generator in a_map.get_codomain().get_generator_list():
        dual_map_domain_list.append(generator)

    for generator in a_map.get_domain().get_generator_list():
        dual_map_codomain_list.append(generator)
    
    for generator in dual_map_domain_list:
        value = ModElt()
        for target in a_map.get_domain().get_generator_list():
            output = a_map.evaluate(target, options)
            coefficient = output.get_generator_coefficient(
                generator.get_summands()[0].get_generator(), options)
            dual_coefficient = coefficient.get_dual(options)
            target_copy = target.copy()
            target_copy.scalar_multiply(dual_coefficient, options)
            value.add(target_copy)
            #        value.expanded_form()
            #        value.combine_monomials(options)
        value.canonical_form(options)
        dual_map_dict[generator.get_summands()[0].get_generator().get_name()] = value
                        
    return FreeHDualModuleMap(
        FreeHDualModule(dual_map_domain_list, 
                        options.get_degree_bounds()), 
        FreeHDualModule(dual_map_codomain_list,
                        options.get_degree_bounds()),
        dual_map_dict)
        
