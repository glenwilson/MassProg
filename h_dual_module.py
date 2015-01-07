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
import copy
import logging
import cPickle as pickle

#Which imports above can be removed?

class FreeHDualModule(object):
    """
    Generates free H dual module in region with bounds deg_bounds =
    (a, b) positive integers, -a <= x and -b <= y. The positive bounds
    being determined by the generators themselves.
    """

    def __init__(self, generator_list, deg_bounds):
        self.generator_list = generator_list
        self.deg_bounds = deg_bounds
        self.array = {}
        self.array_flag = False
        self.h_dual = {}
        self.h_dual_flag = False

    def __getstate__(self):
        return {'generator_list' : self.generator_list, 
                'deg_bounds' : self.deg_bounds,
                'array' : self.array,
                'array_flag' : self.array_flag,
                'h_dual' : self.h_dual,
                'h_dual_flag' : self.h_dual_flag}

    def __setstate__(self, _dict):
        self.generator_list = _dict['generator_list']
        self.deg_bounds = _dict['deg_bounds']
        self.array = _dict['array']
        self.array_flag = _dict['array_flag']
        self.h_dual = _dict['h_dual']
        self.h_dual_flag = _dict['h_dual_flag']

    def get_array(self, options):
        if not self.array:
            self.generate_array(options)
            self.array_flag = True
        elif not self.array_flag:
            self.generate_array(options)
            self.array_flag = True
        return self.array

    def get_generator_list(self):
        return self.generator_list

    def get_deg_bounds(self):
        return self.deg_bounds
    
    def generate_h_dual(self, options):
        self.h_dual = h_dual(2* options.get_degree_bounds()[0] + 2, 
                             2 * options.get_degree_bounds()[1] + 2, 
                             options)
        self.h_dual_flag = True

    def get_h_dual(self, options):
        if not self.h_dual_flag:
            self.generate_h_dual(options)
        return self.h_dual

    def add_generator(self, generator):
        self.generator_list.append(generator)
        self.array_flag = False

    def generate_array(self, options):
        for pair in [(x,y) for x in 
                     range(-self.get_deg_bounds()[0], 
                            self.get_deg_bounds()[0] + 1)
                     for y in range(-self.get_deg_bounds()[1], 
                                     self.get_deg_bounds()[1] + 1) ]:
            self.array[pair] = ModTwoVectorSpace([])
        for generator in self.get_generator_list():
            for gadget in self.get_h_dual(options):
                for coefficient in self.get_h_dual(options)[gadget]:
                    new_element = generator.copy()
                    new_element.scalar_multiply(coefficient, options)
                    new_element.canonical_form(options)
                    if new_element.get_degree(options) in self.array:
                        self.array[new_element.get_degree(options)
                                   ].add_basis_element([new_element])

    def add_generator_update_array(self, generator, options):
        self.generator_list.append(generator)
        for gadget in self.get_h_dual(options):
            for coefficient in self.get_h_dual(options)[gadget]:
                new_element = generator.copy()
                new_element.scalar_multiply(coefficient, options)
                new_element.canonical_form(options)
                if new_element.get_degree(options) in self.array:
                    self.array[new_element.get_degree(options)
                               ].add_basis_element([new_element])

    def element_from_vector(self, position, vector, options):
        """
        Returns the element in the module at "position" corresponding
        to the "vector" according to the ordering of the Z2 basis stored.
        """
        element = ModElt()
        basis = self.get_array(options)[position].get_basis()
        if not basis:
            element.scalar_multiply(RPolynomial(()), options)
            return element
        elif not vector.is_zero():
            for index in range(0, len(vector)):
                if vector[index] == 1:
                    element.add(basis[index])
        else:
            element.scalar_multiply(RPolynomial(()), options)
        return element

    def vector_from_element(self, element, position, options):
        vect_space = self.get_array(options)[position]
        basis_length = len(vect_space.get_basis())
        if not basis_length:
            new_vector = BitVector(1)
            return new_vector
        new_vector = BitVector( basis_length )
        element.canonical_form(options)
        for monomial in element.get_summands():
            flag = False
            for index in xrange( basis_length ):
                thing = vect_space.get_basis()[index]
                if str(monomial) == str(thing):
                    new_vector[index] = 1
                    flag = True
                    break
            if not flag:
                print basis_length
                print element.get_summands()
                print element
                print ("Error, Error! The summand " + str(monomial) + 
                       " does not correspond to a basis element in position " 
                       + str(position))
                raise TypeError
        return new_vector


class MatrixMapStorage(object):
    def __init__(self):
        self.matrix_storage = {}
        self.lock = thread.allocate_lock()
        
    def __getstate__():
        return {'matrix_storage' : self.matrix_storage,
                'lock' : self.lock}

    def __setstate__(_dict):
       self.matrix_storage = _dict['matrix_storage']
       self.lock = _dict['lock']

    def save(self, pair):
        position = pair[0]
        matrix = pair[1]
        self.lock.acquire()
        self.matrix_storage[position] = matrix
        self.lock.release()

    def get_matrix_storage(self):
        return self.matrix_storage

class FreeHDualModuleMap(object):
    def __init__(self, domain, codomain, generator_map):
        """
        Domain and codomain are FreeAModule objects, and generator map
        is a dictionary whose keys are the generator objects of the
        generators of the domain, and the values are module elements
        in the codomain.

        This class can evaluate the function at an element of the
        domain, and produce a matrix for the map in a particular
        graded piece.
        """
        self.domain = domain
        self.codomain = codomain
        self.generator_map = generator_map
        self.matrix_storage = {}

    def __getstate__(self):
        return {'domain' : self.domain, 
                'codomain' : self.codomain, 
                'generator_map' : self.generator_map,
                'matrix_storage' : self.matrix_storage
                }

    def __setstate__(self, _dict):
        self.domain = _dict['domain']
        self.codomain = _dict['codomain']
        self.generator_map = _dict['generator_map']
        self.matrix_storage = _dict['matrix_storage']

    def get_domain(self):
        return self.domain
    
    def get_codomain(self):
        return self.codomain

    def get_generator_map(self):
        return copy.deepcopy(self.generator_map)

    def get_matrix_storage(self):
        return self.matrix_storage

    def get_original_map(self):
        return self.original_map

    def get_correction_term(self, module_monomial, options):
        #may want to incorporate case checking here so don't do lots
        #of unnecessary stuff!
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        value = ModElt()
        logging.debug( "mod monomial value for " + str(module_monomial))
        for term in self.get_generator_map()[module_monomial.get_generator().get_name()].get_summands():
            term_copy = term.copy()
            new_coefficient = term_copy.get_coefficient()
            new_coefficient = new_coefficient * module_monomial.get_coefficient().copy()
            logging.debug(new_coefficient)
            new_coefficient.simplify(options)
            logging.debug(new_coefficient)
            new_coefficient.kill_squares(options)
            term_copy.coefficient = new_coefficient
            logging.debug( "term copy " + str(term_copy))
            value.add(ModElt(term_copy))
        value.canonical_form(options)
        logging.debug( "Value  " + str(value))
        return value
                
    def evaluate(self, module_element, options):
        output_element = ModElt()
        generator_map = self.get_generator_map()
        for summand in module_element.get_summands():
            output_element.add(self.get_correction_term(summand, options))
        output_element.canonical_form(options)
        return output_element

    def compute_map_at(self, position, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.debug("AT POSITION" + str(position))
        domain_space = self.get_domain().get_array(options)[position]
        codomain_space = self.get_codomain().get_array(options)[position]
        matrix_map = []
        if not domain_space.get_basis() and not codomain_space.get_basis():
            new_vector = BitVector(1)
            matrix_map.append(new_vector)
        elif not domain_space.get_basis() and codomain_space.get_basis():
            new_vector = BitVector(len(codomain_space.get_basis()))
            matrix_map.append(new_vector)
        for basis_element in domain_space.get_basis():
            logging.debug("the domain space should be nonempty!")
            logging.debug("  this basis element" + str(basis_element))
            output = self.evaluate(basis_element, options)
            output.canonical_form(options)
            logging.debug("  goes to" + str(output))
            if not codomain_space.get_basis():
                new_vector = BitVector(1)
            else:
                new_vector = BitVector( len(codomain_space.get_basis()))
                for monomial in output.get_summands():              
                    flag = False
                    for index in xrange(0, len(codomain_space.get_basis())):
                        thing = codomain_space.get_basis()[index]
                        if str(monomial) == str(thing):
                            logging.debug("this basis elt hit \n" + str(thing))
                            new_vector[index] = 1
                            flag = True
                            break
                    if not flag:
                        logging.warning("Error, Error! The summand " + str(monomial) + 
                                  " does not correspond to a basis element in position " 
                                  + str(position))
                        print monomial
                        raise TypeError("Something in wrong degree")
            logging.debug("the image vector \n" + str(new_vector))
            matrix_map.append(new_vector)
        output = BitMatrix(matrix_map)
        output.transpose()
        logging.debug("NEW MATRIX: \n" +str(output))
        self.matrix_storage[position] = output

    def compute_map_at_no_save(self, position, options):
        logging.basicConfig(filename=options.get_log_file(), level=options.get_logging_level())
        logging.debug("AT POSITION" + str(position))

        domain_space = self.get_domain().get_array(options)[position]
        codomain_space = self.get_codomain().get_array(options)[position]
        matrix_map = []
        if not domain_space.get_basis() and not codomain_space.get_basis():
            new_vector = BitVector(1)
            matrix_map.append(new_vector)
        elif not domain_space.get_basis() and codomain_space.get_basis():
            new_vector = BitVector(len(codomain_space.get_basis()))
            matrix_map.append(new_vector)
        for basis_element in domain_space.get_basis():
            output = self.evaluate(basis_element, options)
            output.canonical_form(options)
            if not codomain_space.get_basis():
                new_vector = BitVector(1)
            else:
                new_vector = BitVector( len(codomain_space.get_basis()))
                for monomial in output.get_summands():              
                    flag = False
                    for index in xrange(0, len(codomain_space.get_basis())):
                        thing = codomain_space.get_basis()[index]
                        if str(monomial) == str(thing):
                            new_vector[index] = 1
                            flag = True
                            break
                    if not flag:
                        print "trying to find " + str(monomial)
                        print "in list of "
                        for thing in codomain_space.get_basis():
                            print thing
                        
                        raise TypeError("Something in wrong degree")
            matrix_map.append(new_vector)
        output = BitMatrix(matrix_map)
        output.transpose()
        return (position, output)

    def save_matrix_map(self, matrix_map_storage):
        self.matrix_storage = matrix_map_storage.get_matrix_storage()

    def multiprocess_compute_maps(self, options):
        inputs = self.get_domain().get_array(options).keys()
        out_q = Queue()
        numpcs = options.get_numpcs()
        chunksize = len(inputs)/numpcs
        procs = []
        
        for i in range(numpcs + 1):
            p = Process(
                target=worker,
                args=(self, inputs[chunksize * i : chunksize * (i + 1)], options, out_q))
            procs.append(p)
            p.start()
        
        resultdict = {}
        for i in range(numpcs + 1):
            resultdict.update(out_q.get())

        # Wait for all worker processes to finish
        for p in procs:
            p.join()
        for key in resultdict.keys():
            output = resultdict[key]
            self.matrix_storage[output[0]] = output[1]

    def get_map_at(self, position, options):
        if position in self.get_matrix_storage():
            return self.get_matrix_storage()[position]
        else:
            self.compute_map_at(position, options)
            return self.get_matrix_storage()[position]


def worker(amap, positions, options, out_q):
    out_dict = {}
    for position in positions:
        out_dict[position] = amap.compute_map_at_no_save(position, options)
    out_q.put(out_dict)

