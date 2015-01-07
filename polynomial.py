from monomial import Monomial
import copy

class Polynomial(object):
    def __init__(self, tuple_of_monomials):
        self.tuple_of_monomials = ()
        if (type(tuple_of_monomials) == tuple or 
            type(tuple_of_monomials) == list):
            self.tuple_of_monomials = tuple(tuple_of_monomials)
        elif isinstance(tuple_of_monomials, Monomial):
            self.tuple_of_monomials = (tuple_of_monomials, )
        else:
            raise NameError("Incorrect input")

    def __getstate__(self):
        return {'tuple_of_monomials' : self.tuple_of_monomials}

    def __setstate__(self, _dict):
        self.tuple_of_monomials = _dict['tuple_of_monomials']
    
    def get_monomial_tuple(self):
        return self.tuple_of_monomials

    def copy(self):
        """
        Returns deepcopy of self.

        !!! Implement class level def. of deepcopy.
        """
        return copy.deepcopy(self)

    def add(self, polynomial):
        """
        Accepts either polynomial or monomial input. Updates given
        polynomial to have polynomial added to it on right.
        """
        if isinstance(polynomial, Polynomial):
            self.tuple_of_monomials = (self.get_monomial_tuple() + 
                                       polynomial.get_monomial_tuple())
        elif isinstance(polynomial, Monomial):
            self.tuple_of_monomials = (self.get_monomial_tuple() + 
                                       (polynomial,))
        else:
            return TypeError("Input incorrect")

    def __add__(self, other):
        self_copy = self.copy()
        other_copy = other.copy()
        self_copy.add(other_copy)
        return self_copy

    def collect_terms(self):
        """
        This method collects the terms for each monomial
        """
        for monomial in self.get_monomial_tuple():
            monomial.collect_terms()
            
    def remove_zero_monomials(self):
        """
        This method removes any monomial with coefficient 0 mod 2.
        """
        new_tuple = tuple([monomial for monomial in 
                           self.get_monomial_tuple() if 
                           monomial.get_coefficient() != 0 ])
        self.tuple_of_monomials = new_tuple

    def combine_monomials(self):
        """
        This simplification method will simplify mod 2. Updates
        polynomial accordingly. Terms of monomials are collected in
        this method.
        """
        self.collect_terms()
        self.remove_zero_monomials()
        temp_list = list(self.get_monomial_tuple())
        new_tuple = ()
        while temp_list:
            monomial = temp_list[0]
            number = len([ x for x in temp_list if monomial.is_equal_to(x)])
            if number % 2:
                new_tuple = new_tuple + (monomial,)
            else:
                pass
            temp_list = [ x for x in temp_list if not monomial.is_equal_to(x)]
        self.tuple_of_monomials = new_tuple

    def expand_terms(self):
        for monomial in self.get_monomial_tuple():
            monomial.expand_terms()
        

    def _print(self, X="X"):
        if self.get_monomial_tuple():
            out = ""
            for monomial in self.get_monomial_tuple():
                out = out + monomial._print(X) + " + "
            return out[:-3]
        else:
            return "0"

    def __mul__(self,other):
        self_copy = self.copy()
        other_copy = other.copy()
        self_copy.right_multiply(other_copy)
        return self_copy

    def left_multiply(self, polynomial):
        """
        input is a polynomial object. Updates polynomial object to be
        the result of multiplication by polynomial on the left of
        self.
        """
        temp_polynomial = Polynomial(())
        for other_monomial in polynomial.get_monomial_tuple():
            for self_monomial in self.get_monomial_tuple():
                temp_monomial = other_monomial.copy()
                temp_monomial.right_multiply(self_monomial)                
                temp_polynomial.add(temp_monomial)
        self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()

    def right_multiply(self, polynomial):
        """
        input is a SteenrodSq object. Returns a SteenrodSq object
        corresponding to multiplying self by the input on the right.
        """
        temp_polynomial = Polynomial(())
        for self_monomial in self.get_monomial_tuple():
            for other_monomial in polynomial.get_monomial_tuple():
                temp_monomial = self_monomial.copy()
                temp_monomial.right_multiply(other_monomial)
                temp_polynomial.add(temp_monomial)
        self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()

    

    
                
            
        
        
        

    

        
        
