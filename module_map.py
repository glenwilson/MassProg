from r_polynomial import *
from r_monomial import *
from r_steenrod_algebra import *
from generator import Generator
from free_A_module import * 
#from mod_2_matrix import ModTwoMatrix
from bit_vector import BitVector
from bit_matrix import BitMatrix
from vector_space import ModTwoVectorSpace
from pickle_storage import *
from multiprocessing import *
import copy
import logging
import cPickle as pickle
import math
import time
 
class FreeAModuleMap(object):
    def __init__(self, domain, codomain, generator_map, kill_sq=False):
        """Domain and codomain are FreeAModule objects, and generator map
        is a dictionary whose keys are the generator objects of the
        generators of the domain, and the values are module elements
        in the codomain.

        This class can evaluate the function at an element of the
        domain, and produce a matrix for the map in a particular
        graded piece.

        The option kill_sq if set to true will kill all Sq^i's upon
        evaluation. This enables one to encode a map to H** as a "free
        A module map"
        """
        self.domain = domain
        self.codomain = codomain
        self.generator_map = generator_map
        self.matrix_storage = {}
        self.kill_sq = kill_sq

    def __getstate__(self):
        return {'domain' : self.domain, 
                'codomain' : self.codomain, 
                'generator_map' : self.generator_map,
                'matrix_storage' : self.matrix_storage,
                'kill_sq' : self.kill_sq}

    def __setstate__(self, _dict):
        self.domain = _dict['domain']
        self.codomain = _dict['codomain']
        self.generator_map = _dict['generator_map']
        self.matrix_storage = _dict['matrix_storage']
        self.kill_sq = _dict['kill_sq']

    def copy(self):
        return copy.deepcopy(self)

    def get_domain(self):
        return self.domain
    
    def get_codomain(self):
        return self.codomain

    def get_generator_map(self):
        return copy.deepcopy(self.generator_map)

    def get_matrix_storage(self):
        return self.matrix_storage

    def evaluate(self, module_element, options):
        #if found
        #if not found, send to zero
        module_element.combine_monomials(options)
        output_element = ModElt()
        generator_map = self.get_generator_map()
        for summand in module_element.get_summands():
            generator_image = generator_map[summand.get_generator().get_name()].copy()
            generator_image.scalar_multiply(summand.get_coefficient(), 
                                            options)
            output_element.add(generator_image)
        if self.kill_sq:
            output_element.kill_squares(options)
        output_element.canonical_form(options)
        return output_element

    def compose(self, other, options):
        #TODO Test the following. need free a module = test
        #if self.get_domain() != other.get_codomain():
        #      
        new_domain = other.get_domain()
        new_codomain = self.get_codomain()
        generator_map = {}
        for generator in new_domain.get_generator_list():
            stage1 = other.evaluate(generator, options)
            stage1.canonical_form(options)
            output = self.evaluate(stage1, options)
            generator_map[generator.get_summands()[0].get_generator().get_name()] = output
        return FreeAModuleMap(new_domain, new_codomain, generator_map)

    def kill_squares(self, options):
        new_generator_map = {}
        for generator in self.get_domain().get_generator_list():
            output_copy = self.evaluate(generator, options).copy()
            output_copy.kill_squares(options)
            output_copy.canonical_form(options)
            new_generator_map[generator.get_summands()[0].get_generator().get_name()] = output_copy
        self.generator_map = new_generator_map
        self.matrix_storage = {}

    def kill_sq_geq_2(self, options):
        new_generator_map = {}
        for generator in self.get_domain().get_generator_list():
            output_copy = self.evaluate(generator, options).copy()
            output_copy.kill_sq_geq_2(options)
            output_copy.canonical_form(options)
            new_generator_map[generator.get_summands()[0].get_generator().get_name()] = output_copy
        self.generator_map = new_generator_map
        self.matrix_storage = {}

    def multiprocess_make_map_dict(self, position, options):
        domain_space = self.get_domain().get_array(options)[position]
        inputs = domain_space.get_basis()
        out_q = Queue()
        numpcs = options.get_numpcs()
        if len(inputs) <= numpcs:
            chunksize = numpcs + 1
            numpcs = 1
        else:
            chunksize = len(inputs)/numpcs + 1
        procs=[]
#        print str(len(inputs)) + " " + str(chunksize) + " " + str(numpcs)
#        print "starting to compute"
#        print inputs
        for i in range(numpcs):
            p = Process(
                target=map_worker,
                args=(self, 
                      inputs[chunksize * i : chunksize * (i + 1)], 
                      options, out_q))
            procs.append(p)
            p.start()

        resultdict={}
        for i in range(numpcs):
            resultdict.update(out_q.get())
        for p in procs:
            p.join()
        
        storagedict = {}
        for key in resultdict.keys():
            output = resultdict[key]
            storagedict[str(output[0])] = output[1]

        return storagedict

    def compute_map_at(self, position, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        domain_space = self.get_domain().get_array(options)[position]
        codomain_space = self.get_codomain().get_array(options)[position]
        matrix_map = []
        numpcs = options.get_numpcs()
        if not domain_space.get_basis() and not codomain_space.get_basis():
            new_vector = BitVector(1)
            matrix_map.append(new_vector)
        elif not domain_space.get_basis() and codomain_space.get_basis():
            new_vector = BitVector(len(codomain_space.get_basis()))
            matrix_map.append(new_vector)
        if len(domain_space.get_basis()) <= 2 * numpcs or numpcs == 1:
            storagedict = {}
            for basis_element in domain_space.get_basis():
                logging.debug("  this basis element" + str(basis_element))
                output = self.evaluate(basis_element, options)
                storagedict[str(basis_element)] = output
        else:
            storagedict = self.multiprocess_make_map_dict(position, options)
        for basis_element in domain_space.get_basis():
            output = storagedict[str(basis_element)]
            if not codomain_space.get_basis():
                new_vector = BitVector(1)
            else:
                new_vector = self.get_codomain().vector_from_element(output, position, options)
            logging.debug("the image vector \n" + str(new_vector))
            matrix_map.append(new_vector)
        output = BitMatrix(matrix_map)
        output.transpose()
        self.matrix_storage[position] = output

    def get_map_at(self, position, options):
        if position in self.get_matrix_storage():
            return self.get_matrix_storage()[position]
        else:
            self.compute_map_at(position, options)
            return self.get_matrix_storage()[position]

    def get_next_resolvant(self, gen_name, options):
        logging.basicConfig(filename=options.get_log_file(), 
                            level=options.get_logging_level())
        size = options.get_degree_bounds()
        next_module = FreeAModule([], size)
        next_map_dict = {}
        next_map = FreeAModuleMap(next_module, self.get_domain(), 
                                  next_map_dict)
        key_list = self.get_domain().get_array(options).keys()
        key_list.sort()
        key_list.reverse()
        key_list = sorted(key_list, key=lambda entry: (entry[0] + entry[1]))
        key_list = [ key for key in key_list if key[0] >= 2 * key[1] ]
        for position in key_list:
            counter = 0
            matrix = self.get_map_at(position, options)
            logging.warning(str(position))
            logging.warning("matrix of self map")
            logging.debug("\n" + str(matrix))
            logging.warning("size is " +str(matrix.get_size()))
            logging.warning("getting kernel")
            kernel = ModTwoVectorSpace(matrix.get_kernel())
            logging.warning("kernel has dimension " 
                            + str(len(kernel.get_basis())))
            logging.warning("getting next matrix")
            next_matrix = next_map.get_map_at(position, options)
            logging.warning("matrix of next map")
            logging.debug("\n" + str(next_matrix))
            logging.warning("size is " + str(next_matrix.get_size()))
            logging.warning("rank is " + str(next_matrix.get_rank()))
            if len(kernel.get_basis()) != next_matrix.get_rank():
                for vector in kernel.get_basis():
                    if not self.get_domain().get_array(options)[position].get_basis():
                        break
                    logging.warning("checking if vector " + str(vector) + 
                              " was hit")
                    logging.debug(str(self.get_domain(
                            ).element_from_vector(position, 
                                                  vector, options)))
                    logging.warning("starting to check for solutions")
                    if next_matrix.can_solve(vector):
                        logging.warning("True")
                    else:
                        to_hit = self.get_domain().element_from_vector(
                            position, vector, options)
                        new_generator = ModElt(ModuleMonomial(RSq(), Generator(
                                    gen_name + str(position) + str(counter), 
                                    position )))
                        logging.warning("new generator")
                        logging.warning(str(new_generator.get_summands(
                                    )[0].get_generator().get_name()))
                        counter = counter + 1
                        logging.warning("updating array")
                        next_module.add_generator_update_array(new_generator, options)
                        next_map_dict[ new_generator.get_summands(
                                )[0].get_generator().get_name() ] = to_hit
                        logging.warning("computing map")
                        next_map.compute_map_at(position, options)
        return next_map

    def extend_next_resolvant(self, resolvant, gen_name, new_bounds, options):
        logging.basicConfig(filename=options.get_log_file(), 
                            level=options.get_logging_level())
        old_size = options.get_degree_bounds()
        next_map = resolvant.copy()
        self.get_domain().increase_bounds(new_bounds, options)
        self.get_codomain().increase_bounds(new_bounds, options)
        next_map.get_domain().increase_bounds(new_bounds, options)
        next_map.codomain = self.get_domain()

        key_list = self.get_domain().get_array(options).keys()
        key_list.sort()
        key_list.reverse()
        key_list = sorted(key_list, key=lambda entry: (entry[0] + entry[1]))
        key_list = [ key for key in key_list if key[0] >= 2 * key[1] ]
        key_list = [ key for key in key_list if (key[0] >= old_size[0] 
                                                 or key[1] >= old_size[1])]
        for position in key_list:
            counter = 0
            matrix = self.get_map_at(position, options)
            logging.warning(str(position))
            logging.warning("matrix of self map")
            logging.debug("\n" + str(matrix))
            logging.warning("size is " +str(matrix.get_size()))
            kernel = ModTwoVectorSpace(matrix.get_kernel())
            logging.warning("kernel has dimension " 
                            + str(len(kernel.get_basis())))
            next_matrix = next_map.get_map_at(position, options)
            logging.warning("matrix of next map")
            logging.debug("\n" + str(next_matrix))
            logging.warning("size is " + str(next_matrix.get_size()))
            logging.warning("rank is " + str(next_matrix.get_rank()))
            if len(kernel.get_basis()) != next_matrix.get_rank():
                for vector in kernel.get_basis():
                    if not self.get_domain().get_array(options)[position].get_basis():
                        break
                    logging.warning("checking if vector " + str(vector) + 
                                    " was hit")
                    logging.debug(str(self.get_domain(
                                ).element_from_vector(position, 
                                                      vector, options)))
                    if next_matrix.can_solve(vector):
                        logging.warning("True")
                    else:
                        to_hit = self.get_domain().element_from_vector(
                            position, vector, options)
                        new_generator = ModElt(ModuleMonomial(RSq(), Generator(
                                    gen_name + str(position) + str(counter), 
                                    position )))
                        logging.warning("new generator")
                        logging.warning(str(new_generator.get_summands(
                                    )[0].get_generator().get_name()))
                        counter = counter + 1
                        logging.warning("updating array")
                        next_map.get_domain().add_generator_update_array(new_generator, options)
                        next_map.generator_map[ new_generator.get_summands(
                                )[0].get_generator().get_name() ] = to_hit
                        logging.warning("computing map")
                        next_map.compute_map_at(position, options)
        return next_map

def map_worker(amap, basis_elements, options, out_q):
    out_dict = {}
    for basis_element in basis_elements:
        out_dict[str(basis_element)] = (basis_element, amap.evaluate(basis_element, options))
    out_q.put(out_dict)

                    
class Resolution(object):
    def __init__(self, map_list, options):
        self.map_list = map_list

    def __getstate__(self):
        return {'map_list' : self.map_list}

    def __setstate__(self, _dict):
        self.map_list = _dict['map_list']

    def get_map_list(self):
        return self.map_list
    
    def get_length(self):
        return len(self.get_map_list())+1

    def kill_squares(self, options):
        for a_map in self.get_map_list():
            a_map.kill_squares(options)

    def kill_sq_geq_2(self, options):
        for a_map in self.get_map_list():
            a_map.kill_sq_geq_2(options)

    def map_printout(self, filename, optiosn):
        out_string = ""
        counter = 0
        for a_map in self.get_map_list():
            out_string = (out_string + "Map " + str(counter) 
                          + " : \n")
            for generator in sorted(a_map.get_generator_map()):
                out_string = (out_string + str(generator) + " --> " 
                              + str(a_map.get_generator_map()[generator]) 
                              + "\n")
            counter = counter + 1
        _file = open(filename, 'w+')
        _file.write(out_string)
        _file.close()

def make_initial_map(options):
    iota = (ModuleMonomial(RSq(), Generator("i", (0,0))))
    jot = (ModuleMonomial(RSq(), Generator("j", (0,0))))
    F0 = FreeAModule([ModElt(iota)], 
                     options.get_degree_bounds())
    H = FreeAModule([ModElt(jot)], options.get_degree_bounds())
    map_dict = {}
    map_dict[iota.get_generator().get_name()] = ModElt(jot)
    f = FreeAModuleMap(F0, H, map_dict, True)
    next_map = f.get_next_resolvant("h1", options)
    return next_map

def extend_initial_map(bounds, options):
    iota = (ModuleMonomial(RSq(), Generator("i", (0,0))))
    jot = (ModuleMonomial(RSq(), Generator("j", (0,0))))
    F0 = FreeAModule([ModElt(iota)], 
                     options.get_degree_bounds())
    H = FreeAModule([ModElt(jot)], options.get_degree_bounds())
    map_dict = {}
    map_dict[iota.get_generator().get_name()] = ModElt(jot)
    f = FreeAModuleMap(F0, H, map_dict, True)
    F0_prime = FreeAModule([ModElt(iota)], 
                     bounds)
    H_prime = FreeAModule([ModElt(jot)], bounds)
    f_prime = FreeAModuleMap(F0_prime, H_prime, map_dict, True)
    print "f prime's kill_sq"
    print f_prime.kill_sq
    next_map = f.get_next_resolvant("h1",options)
    extended_map = f_prime.extend_next_resolvant(next_map, "h1", bounds, options)
    return extended_map

# def extend_initial_map(bounds, options):
#     iota = (ModuleMonomial(RSq(), Generator("i", (0,0))))
#     F0 = FreeAModule([ModElt(iota)], bounds)
#     generator_list = []
#     map_dict = {}
#     if options.get_case() == "Classical":
#         upper_bound = int(math.log(bounds[0], 2))
#     else:
#         upper_bound = int(min(math.log(bounds[0], 2), 
#                               math.log(2 * bounds[1], 2))) 
#     for index in range(0, upper_bound + 1):
#         name = "a" + str(2**index)
#         print name
#         print 2**index/2
#         if options.get_case() == "Classical":
#             generator_list.append(
#                 ModElt((ModuleMonomial(
#                             RSq(), 
#                             Generator(name, (2**index, 0))))))
#         else:
#             generator_list.append(
#                 ModElt((ModuleMonomial(
#                             RSq(), 
#                             Generator(name, (2**index, 2**index/2))))))
#         temp = ModElt(iota).copy()
#         temp.scalar_multiply(RSq(2**index), options)
#         print temp
#         map_dict[generator_list[-1].get_summands()[0].get_generator().get_name()] = temp
#         print map_dict[ name ]
#         print map_dict [ generator_list[-1].get_summands()[0].get_generator().get_name() ]
#     F1 = FreeAModule(generator_list, bounds)
#     output_map = FreeAModuleMap(F1, F0, map_dict)
#     return output_map





    
    
    
