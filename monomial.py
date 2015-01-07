import copy

class Monomial(object):
    def __init__(self, tuple_of_terms, coefficient):
        """
        Preferred input format is a tuple of pairs (object,
        exponent). Object can be either a string or integer. If an
        integer, it is considered as an indexed variable Sq^i.
        """
        self.coefficient = coefficient % 2 
        if self.coefficient == 0:
            self.tuple_of_terms = ()
        else:
            self.tuple_of_terms = tuple_of_terms

    def __getstate__(self):
        return {'tuple_of_terms' : self.tuple_of_terms,
                'coefficient' : self.coefficient}
        
    def __setstate__(self, _dict):
        self.tuple_of_terms = _dict['tuple_of_terms']
        self.coefficient = _dict['coefficient']

    def get_coefficient(self):
        return self.coefficient

    def get_terms(self):
        return self.tuple_of_terms

    def get_expanded_tuple(self):
        """
        returns a tuple where all factors appear to the power 1.
        Output is of the form ((obj, n), (obj, n), ... )
        """
        output_tuple = ()
        for term in self.get_terms():
            output_tuple = output_tuple + term[1]*((term[0], 1),)
        return output_tuple

    def get_expanded_terms(self):
        """
        Returns tuple (obj, obj, obj, ...)
        """
        output_tuple = ()
        for pair in self.get_terms():
            output_tuple = output_tuple + pair[1]*(pair[0],)
        return output_tuple

    def is_equal_to(self, monomial):
        return (self.get_terms() == monomial.get_terms() and 
                self.get_coefficient() == monomial.get_coefficient())

    def copy(self):
        """
        Returns a deepcopy of the object

        !!! Implement class level def. of copy and deepcopy to better
        control what is copied.
        """
        return copy.deepcopy(self)

    def _print(self, X="X"):
        """
        Returns a string representing the monomial. If integer
        variables are used, they are represented as Xn, where n is the
        integer, unless the default option is changed.
        """
        output = ""
        if self.get_coefficient() and self.get_terms():
            for term in self.get_terms():
                if type(term[0]) == str:
                    if term[1] != 1:
                        output = output + term[0] + "^" + str(term[1])
                    else:
                        output = output + term[0]
                elif type(term[0]) == int:
                    if term[1] != 1:
                        output = output + X + str(term[0]) + "^" + str(term[1])
                    else:
                        output = output + X + str(term[0])
        elif self.get_coefficient() and not self.get_terms():
            output = "1"
        else:
            output = "0"
        return output

    def collect_terms(self): 
        """
        This method combines all neighboring terms which are the same
        into one term.
        """
        iteration_list = [ element for element in 
                           self.get_expanded_terms() ] 
        output_tuple = ()
        while iteration_list:
            output_tuple = output_tuple + ((iteration_list[0], 
                                            repeats(iteration_list)),)
            iteration_list = iteration_list[repeats(iteration_list):]
        self.tuple_of_terms = output_tuple

    def expand_terms(self):
        """
        This method expands all terms so that all terms appear only with
        exponent 1. 
        """
        output_tuple = ()
        for term in self.get_terms():
            output_tuple = output_tuple + term[1]*((term[0], 1),)
        self.tuple_of_terms = output_tuple
    
    def left_multiply(self, monomial):
        """
        multiplies monomial to the left of self. Updates self to this
        new monomial.
        """
        self.tuple_of_terms = (monomial.get_terms() + 
                               self.get_terms())
        self.coefficient = monomial.get_coefficient() * self.get_coefficient()
        
    def right_multiply(self, monomial):
        """
        multiplies monomial to the right of self. Updates self to this
        new monomial.
        """
        self.tuple_of_terms = (self.get_terms() + 
                               monomial.get_terms())
        self.coefficient = self.get_coefficient() * monomial.get_coefficient()

    

def repeats(lst):
    """Returns the length of the longest initial segment of the list
    for which all the entries are the same. (This can be improved.)
    """
    if lst == []:
        return 0
    else:
        counter = 0
        for i in range(len(lst)):
            if lst[0] == lst[i]:
                counter = counter + 1
            else:
                break
        return counter   
    
