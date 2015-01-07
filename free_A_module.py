from r_polynomial import *
from r_monomial import *
from r_steenrod_algebra import *
from generator import Generator
from bit_vector import BitVector
from bit_matrix import BitMatrix
from vector_space import ModTwoVectorSpace
import copy

class ModuleMonomial(object):
    """
    To do: Degree assumes r_polynomial is homogeneous. 
    """

    def __init__(self, r_polynomial, generator):
        self.coefficient = r_polynomial
        self.generator = generator

    def __str__(self):
        return (self.get_coefficient().r_print() + "." + 
                self.get_generator().get_name())

    def __getstate__(self):
        return {'coefficient' : self.coefficient, 
                'generator' : self.generator}

    def __setstate__(self, _dict):
        self.coefficient = _dict['coefficient']
        self.generator = _dict['generator']

    def copy(self):
        return copy.deepcopy(self)

    def is_equal_to(self, other):
        return (self.get_name() == other.get_name())

    def get_name(self):
        return (self.get_coefficient().r_print() + "." + 
                self.get_generator().get_name())

    def get_degree(self, options):
        return vector_addition(self.get_coefficient().get_degree_pair(
                options), self.get_generator().get_degree(options))

    def get_coefficient(self):
        return self.coefficient

    def get_generator(self):
        return self.generator

    def scalar_multiply(self, r_polynomial, options):
        old_coefficient = self.get_coefficient()
        new_coefficient = r_polynomial * old_coefficient
        new_coefficient.simplify(options)
        self.coefficient = new_coefficient

    def simplify_coefficient(self, options):
        self.get_coefficient().simplify(options)

    def kill_squares(self, options):
        self.get_coefficient().kill_squares(options)
        self.simplify_coefficient(options)

    def kill_sq_geq_2(self, options):
        self.get_coefficient().kill_sq_geq_2(options)
        self.simplify_coefficient(options)

class ModuleElement(object):
    def __init__(self, list_of_summands):
        self.summands = [ x.copy() for x in list_of_summands ]

    def __getstate__(self):
        return {'summands' : self.summands}

    def __setstate__(self, _dict):
        self.summands = _dict['summands']
    
    def get_summands(self):
        return self.summands

    def copy(self):
        return copy.deepcopy(self)

    def add(self, other):
        self.summands =  self.get_summands() + other.get_summands()

    def __add__(self, other):
        self_copy = self.copy()
        self_copy.add(other)
        return self_copy

    def __str__(self):
        output = ""
        for summand in self.get_summands():
            output = output + str(summand) + " + "
        return output[:-3]
        
    def get_degree_list(self, options):
        output = []
        for monomial in self.get_summands():
            output.append(monomial.get_degree(options))
        if output:
            return output
        else:
            return [(0,0)]

    def get_degree(self, options):
        for pair in self.get_degree_list(options):
            if self.get_degree_list(options)[0] == pair:
                pass
            else:
                return self.get_degree_list(options)
        return self.get_degree_list(options)[0]

    def simplify_coefficient(self, options):
        for summand in self.get_summands():
            summand.simplify_coefficient(options)

    def combine_monomials(self, options):
#TODO is copy necessary here?
#        self_copy = self.copy()
#        self_copy.expanded_form()
        new_module_element = ModElt()
        for monomial in self.get_summands():
            flag = False
            for combined_monomial in new_module_element.get_summands():
                if (monomial.get_generator().get_name() == 
                    combined_monomial.get_generator().get_name()):
                    combined_monomial.get_coefficient().add(
                        monomial.get_coefficient())
                    flag = True
            if not new_module_element.get_summands() or not flag:
                new_module_element.add(ModElt(monomial))       
        new_module_element.simplify_coefficient(options)
        self.summands = new_module_element.get_summands()

    def canonical_form(self, options):
        self.combine_monomials(options)
        self.simplify_coefficient(options)
        new_element = ModElt()
        for summand in self.get_summands():
            if summand.get_coefficient().r_print() == "0":
                pass
            else:
                new_element.add(ModElt(summand))
        new_element.expanded_form()
        self.summands = new_element.get_summands()

    def scalar_multiply(self, r_polynomial, options):
        for summand in self.get_summands():
            summand.scalar_multiply(r_polynomial, options)

    def expanded_form(self):
        self.summands = self.get_expanded_form().get_summands()

    def get_expanded_form(self):
        new_mod_elt = ModElt()
        for summand in self.get_summands():
            for monomial in summand.get_coefficient().get_monomial_tuple():
                new_mod_elt.add(
                    ModElt(ModuleMonomial(RPolynomial(monomial), 
                                          summand.get_generator())))
        return new_mod_elt
    
    def kill_squares(self, options):
        for summand in self.get_summands():
            summand.kill_squares(options)

    def kill_sq_geq_2(self, options):
        for summand in self.get_summands():
            summand.kill_sq_geq_2(options)

    def get_generator_coefficient(self, generator, options):
        self.canonical_form(options)
        self.combine_monomials(options)
        for summand in self.get_summands():
            if summand.get_generator().get_name() == generator.get_name():
                return summand.get_coefficient()
        return RPolynomial(())

    def make_dual(self, options):
        for summand in self.get_summands():
            summand.get_coefficient().make_dual(options)
        
    def make_standard(self, options):
        for summand in self.get_summands():
            summand.get_coefficient().make_standard(options)

                
def ModElt(*args):
    output = ModuleElement([])
    for element in args:
        output.summands = output.get_summands() + [element]
    return output

def ModEltList(a_list):
    output = ModuleElement([])
    for element in a_list:
        output.summands = output.get_summands() + [element]
    return output

class FreeAModule(object):
    def __init__(self, generator_list, deg_bounds):
        self.generator_list = generator_list
        self.deg_bounds = deg_bounds
        self.array = {}
        self.array_flag = False
#        self.generate_array()

    def __getstate__(self):
        return {'generator_list' : self.generator_list, 
                'deg_bounds' : self.deg_bounds,
                'array' : self.array,
                'array_flag' : self.array_flag}

    def __setstate__(self, _dict):
        self.generator_list = _dict['generator_list']
        self.deg_bounds = _dict['deg_bounds']
        self.array = _dict['array']
        self.array_flag = _dict['array_flag']

    def get_array(self, options):
        if not self.array:
            self.generate_array(options)
            self.array_flag = True
        elif not self.array_flag:
            self.generate_array(options)
            self.array_flag = True
        return self.array

    def get_zero_element(self):
        return ModElt()

    def get_generator_list(self):
        return self.generator_list

    def get_deg_bounds(self):
        return self.deg_bounds

    def add_generator(self, generator):
        self.generator_list.append(generator)
        self.array_flag = False

    # def generate_a_star(self, options):
    #     self.a_star = a_star(self.get_deg_bounds()[0] + 1,
    #                          self.get_deg_bounds()[1] + 1, options)
    #     self.a_star_flag = True
        
    def get_a_star(self, options, bounds = None):
        return options.get_a_star(bounds)

    def increase_bounds(self, new_bounds, options):
        old_bounds = self.get_deg_bounds()
        self.deg_bounds = new_bounds
        for pair in [ (x, y) for x in range(0, new_bounds[0]+1 ) \
                          for y in range(0, new_bounds[1]+1 ) \
                          if (x >= old_bounds[0] \
                                  or y >= old_bounds[1])]:
            self.array[pair] = ModTwoVectorSpace([])
        for generator in self.get_generator_list():
            for pair in [ (x, y) for x in range(generator.get_degree(options)[0], 
                                                new_bounds[0]+1) 
                          for y in range(generator.get_degree(options)[1], 
                                         new_bounds[1]+1) 
                          if (x >= old_bounds[0] or y >= old_bounds[1])]:
                for coefficient in options.get_a_star(new_bounds)[
                    (pair[0] - generator.get_degree(options)[0], 
                     pair[1] - generator.get_degree(options)[1])]:
                    new_element = generator.copy()
                    new_element.scalar_multiply(coefficient, options)
                    new_element.canonical_form(options)
                    self.array[pair].add_basis_element([new_element])

    def generate_array(self, options):
        for pair in [(x,y) for x in 
                     range(0, self.get_deg_bounds()[0] + 1)
                     for y in range(0, self.get_deg_bounds()[1] + 1) ]:
            self.array[pair] = ModTwoVectorSpace([])
        for generator in self.get_generator_list():
            for gadget in self.get_a_star(options):
                for coefficient in self.get_a_star(options)[gadget]:
                    new_element = generator.copy()
                    new_element.scalar_multiply(coefficient, options)
                    new_element.canonical_form(options)
                    if new_element.get_degree(options) in self.array:
                        self.array[new_element.get_degree(options)
                                   ].add_basis_element([new_element])

    def add_generator_update_array(self, generator, options):
        self.generator_list.append(generator)
        for gadget in [(x, y) for x in range(0, self.get_deg_bounds()[0] 
                                             - generator.get_degree(options)[0] 
                                             + 1) 
                       for y in range(0, self.get_deg_bounds()[1] 
                                      - generator.get_degree(options)[1] 
                                      + 1)]:
            for coefficient in self.get_a_star(options)[gadget]:
                coefficient = coefficient.copy()
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
        if not position in self.get_array(options):
            new_vector = BitVector(1)
            return new_vector
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


def admissible_monomials(n):
    output = []
    if n == 0:
        return [()]
    for k in range(max(n / 2, 1), n + 1):
        for partition in admissible_monomials(n-k):
            if partition and k >= 2 * partition[0]:
                new_monomial = (k,) + partition
                output.append(new_monomial)
            elif not partition:
                new_monomial = (k,) + partition
                output.append(new_monomial)
            else:
                pass
    return output

def old_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            for pair in [(a, b) for a in range(0, n + 1) for 
                         b in range(0, n + 1)]:
                if monomial:
                    temp_poly = RSqTuple(monomial)
                else:
                    temp_poly = RPolynomial((RMonomial((),1)))
                temp_poly.left_multiply(RPolynomial(
                        RMonomial(((options.get_t(),pair[0]),(options.get_p(),pair[1])),1)))
                temp_poly.collect_terms()
                temp_poly.simplify(options)
                degree = temp_poly.get_degree_pair(options)
                if degree[0] <= n and degree[1] <= m:
                    output[degree] = output[degree] + (temp_poly,)
                else:
                    pass
    return output

def a_star(n, m, options):
    if options.get_case() == "Real":
        return real_a_star(n, m, options)
    elif options.get_case() == "Complex":
        return complex_a_star(n, m, options)
    elif options.get_case() == "Classical":
        return classical_a_star(n, m, options)
    elif options.get_case() == "FiniteOdd3":
        return finite_odd_3_a_star(n, m, options)
    elif options.get_case() == "FiniteOdd1":
        return finite_odd_1_a_star(n, m, options)

def real_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            if monomial:
                temp_poly = RSqTuple(monomial)
            else:
                temp_poly = RPolynomial((RMonomial((),1)))
            monomial_degree = temp_poly.get_degree_pair(options)
            for pair in [(a, b) for a in range(0, m - monomial_degree[1] + 1) 
                         for b in range(0, n - monomial_degree[0] + 1) 
                         if (a + b + monomial_degree[1] <= m)]:
                temp_poly_copy = temp_poly.copy()
                temp_poly_copy.left_multiply(RPolynomial(
                        RMonomial(
                            ((options.get_t(), pair[0]), 
                             (options.get_p(), pair[1]))
                            ,1)
                        ))
                temp_poly_copy.collect_terms()
                temp_poly_copy.simplify(options)
                degree = temp_poly_copy.get_degree_pair(options)
                if degree[0] <= n and degree[1] <= m:
                    output[degree] = output[degree] + (temp_poly_copy,)
                else:
                    pass
    return output

def finite_odd_3_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            if monomial:
                temp_poly = RSqTuple(monomial)
            else:
                temp_poly = RPolynomial((RMonomial((),1)))
            monomial_degree = temp_poly.get_degree_pair(options)
            for pair in [(a, b) for a in \
                         range(0, m - monomial_degree[1] + 1) \
                         for b in \
                         range(0, min(n - monomial_degree[0] + 1, 2)) \
                         if (a + b + monomial_degree[1] <= m)]:
                temp_poly_copy = temp_poly.copy()
                temp_poly_copy.left_multiply(RPolynomial(
                        RMonomial(
                            ((options.get_t(), pair[0]), 
                             (options.get_p(), pair[1]))
                            ,1)
                        ))
                temp_poly_copy.collect_terms()
                # is simplify necessary?
                temp_poly_copy.simplify(options)
                degree = temp_poly_copy.get_degree_pair(options)
                if (degree[0] <= n and degree[1] <= m
                    and temp_poly_copy.is_monomial() 
                    and temp_poly_copy.get_monomial_tuple()[0].get_coefficient()):
                    output[degree] = output[degree] + (temp_poly_copy,)
                else:
                    pass
    return output

def finite_odd_1_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            if monomial:
                temp_poly = RSqTuple(monomial)
            else:
                temp_poly = RPolynomial((RMonomial((),1)))
            monomial_degree = temp_poly.get_degree_pair(options)
            for pair in [(a, b) for a in \
                         range(0, m - monomial_degree[1] + 1) \
                         for b in \
                         range(0, min(n - monomial_degree[0] + 1, 2)) \
                         if (a + b + monomial_degree[1] <= m)]:
                temp_poly_copy = temp_poly.copy()
                temp_poly_copy.left_multiply(RPolynomial(
                        RMonomial(
                            ((options.get_t(), pair[0]), 
                             (options.get_u(), pair[1]))
                            ,1)
                        ))
                temp_poly_copy.collect_terms()
                # is simplify necessary?
                temp_poly_copy.simplify(options)
                degree = temp_poly_copy.get_degree_pair(options)
                if (degree[0] <= n and degree[1] <= m
                    and temp_poly_copy.is_monomial() 
                    and temp_poly_copy.get_monomial_tuple()[0].get_coefficient()):
                    output[degree] = output[degree] + (temp_poly_copy,)
                else:
                    pass
    return output

def complex_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            if monomial:
                temp_poly = RSqTuple(monomial)
            else:
                temp_poly = RPolynomial((RMonomial((),1)))
            monomial_degree = temp_poly.get_degree_pair(options)
            for pair in [(a, 0) for a in range(0, m - monomial_degree[1] + 1)]:
                temp_poly_copy = temp_poly.copy()
                temp_poly_copy.left_multiply(RPolynomial(
                        RMonomial(
                            ((options.get_t(), pair[0]), 
                             (options.get_p(), pair[1]))
                            ,1)
                        ))
                temp_poly_copy.collect_terms()
                temp_poly_copy.simplify(options)
                degree = temp_poly_copy.get_degree_pair(options)
                if degree[0] <= n and degree[1] <= m:
                    output[degree] = output[degree] + (temp_poly_copy,)
                else:
                    pass
    return output

def classical_a_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        output[pair] = ()
    for k in range(0, n+1):
        for monomial in admissible_monomials(k):
            if monomial:
                temp_poly = RSqTuple(monomial)
            else:
                temp_poly = RPolynomial((RMonomial((),1)))
            monomial_degree = temp_poly.get_degree_pair(options)
            temp_poly_copy = temp_poly.copy()
            temp_poly_copy.collect_terms()
            degree = temp_poly_copy.get_degree_pair(options)
            if degree[0] <= n and degree[1] <= m:
                output[degree] = output[degree] + (temp_poly_copy,)
    return output
