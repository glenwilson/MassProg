from monomial import Monomial

class RMonomial(Monomial):
    """
    Assumes the tuple of terms only uses objects t, p (determined in
    options class), and natural numbers.
    """
    def r_print(self):
        return self._print("Sq")

    def get_degree(self, options):
        degree = (0,0)
        for term in self.get_terms():
            if term[0] in options.get_degree_dictionary(): 
                degree = vector_addition(degree, scalar_multiply(
                        term[1], options.get_degree_dictionary()[term[0]]))
            elif type(term[0]) == int:
                degree = vector_addition(degree, scalar_multiply(
                        term[1], degree_function(term[0])))
        ###cases
        if options.get_case() == "Classical":
            degree = (degree[0], 0)
        ###
        return degree

    def case_modification(self, options):
        """
        This method updates a monomial to reflect the case the user is
        working in, either Real, Complex, or Classical. It should be
        run after any update to an object.
        """
        if options.get_case() == "Real":
            pass

        elif options.get_case() == "Complex":
            for term in self.get_terms():
                if term[0] == options.get_p() and term[1] != 0:
                    self.tuple_of_terms = ()
                    self.coefficient = 0
            self.move_taus_left(options)
            temp_tuple = tuple([ term for term in self.get_terms() if 
                                 term[0] != options.get_p() ])
            self.tuple_of_terms = temp_tuple

        elif options.get_case() == "Classical":
            for term in self.get_terms():
                if term[0] == options.get_p() and term[1] != 0:
                    self.tuple_of_terms = ()
                    self.coefficient = 0
            temp_tuple = tuple([ term for term in self.get_terms() if 
                                 (term[0] != options.get_t() and 
                                  term[0] != options.get_p()) ])
            self.tuple_of_terms = temp_tuple

        elif options.get_case() == "FiniteOdd3":
            self_copy = self.copy()
            self_copy.collect_terms()
            for term in self.get_terms():
                if (term[0] == options.get_p() and term[1]>= 2):
                    self.tuple_of_terms = ()
                    self.coefficient = 0
                    break 

        elif options.get_case() == "FiniteOdd1":
            self_copy = self.copy()
            self_copy.collect_terms()
            for term in self.get_terms():
                if (term[0] == options.get_p() and term[1] != 0):
                    self.tuple_of_terms = ()
                    self.coefficient = 0
                    break 
                elif (term[0] == options.get_u() and term[1] >= 2):
                    self.tuple_of_terms = ()
                    self.coefficient = 0
                    break 

    def is_standard(self, options):
        """
        returns true if only has standard p, t terms.
        """
        for term in self.get_terms():
            if term[0] == options.get_t_dual():
                return False
            elif term[0] == options.get_p_dual():
                return False
            elif term[0] == options.get_u_dual():
                return False
        return True

    def dualize(self, options):
        new_terms = ()
        for pair in self.get_terms():
            if pair[0] == options.get_t():
                new_pair = (options.get_t_dual(), pair[1])
                new_terms = new_terms + (new_pair, )
            elif pair[0] == options.get_p():
                new_pair = (options.get_p_dual(), pair[1])
                new_terms = new_terms + (new_pair, )
            elif pair[0] == options.get_u():
                new_pair = (options.get_u_dual(), pair[1])
                new_terms = new_terms + (new_pair, )
            else:
                new_terms = new_terms + (pair, )
        self.tuple_of_terms = new_terms

    def get_dualized_monomial(self, options):
        self_copy = self.copy()
        self_copy.dualize(options)
        return self_copy

    def is_dual(self, options):
        """
        returns true only if has dual p* and t* terms.
        """
        for term in self.get_terms():
            if term[0] == options.get_t():
                return False
            elif term[0] == options.get_p():
                return False
            elif term[0] == options.get_u():
                return False
        return True

    def make_dual(self, options):
        if not self.is_standard(options):
            raise TypeError("not in standard notation")
        new_tuple_of_terms = ()
        for term in self.get_terms():
            if term[0] == options.get_t():
                new_term = (options.get_t_dual(), term[1])
                new_tuple_of_terms = new_tuple_of_terms + (new_term,)
            elif term[0] == options.get_p():
                new_term = (options.get_p_dual(), term[1])
                new_tuple_of_terms = new_tuple_of_terms + (new_term,)
            elif term[0] == options.get_u():
                new_term = (options.get_u_dual(), term[1])
                new_tuple_of_terms = new_tuple_of_terms + (new_term,)
            else:
                new_tuple_of_terms = new_tuple_of_terms + (term, )
        self.tuple_of_terms = new_tuple_of_terms 

    def make_standard(self, options):
        if not self.is_dual(options):
            raise TypeError("not in dual notation")
        new_tuple_of_terms = ()
        for term in self.get_terms():
            if term[0] == options.get_t_dual():
                new_tuple_of_terms = new_tuple_of_terms + ((options.get_t(), term[1]),)
            elif term[0] == options.get_p_dual():
                new_tuple_of_terms = new_tuple_of_terms + ((options.get_p(), term[1]),)
            elif term[0] == options.get_u_dual():
                new_tuple_of_terms = new_tuple_of_terms + ((options.get_u(), term[1]),)

            else:
                new_tuple_of_terms = new_tuple_of_terms + (term, )
        self.tuple_of_terms = new_tuple_of_terms 

    def get_dual(self, options):
        self_copy = self.copy()
        self_copy.make_dual(options)
        return self_copy

    def get_standard(self, options):
        self_copy = self.copy()
        self_copy.make_standard(options)
        return self_copy

    def remove_square_zeros(self):
        """
        removes square zeros
        """
        self.tuple_of_terms = tuple([ pair for pair in 
                                      self.get_terms() if pair[0] != 0])

    def remove_squares(self):
        self.tuple_of_terms = tuple([pair for pair in 
                                     self.get_terms() 
                                     if type(pair[0]) != int])

    def first_square_index(self):
        """
        Returns the index i where self.get_tuple()[i] is the first
        term from the left corresponding to a Sq generator.
        
        Returns None if the monomial does not contain any Sq's. 
        """
        for index in xrange(0, len(self.get_terms())):
            if type(self.get_terms()[index][0]) == int:
                return index
            else:
                pass
        return None

    def is_admissible(self):
        """
        !!! Potentially different than what you would expect. This
            allows elements of the ground ring to appear on the left.

        Returns true if all p, t terms are on the left, and if the
        Sqi's form an admissible sequence. That is, i_(j+1) >= 2i_j
        for all positions j where j and j+1 are integers.
        """
        temp_monomial = RMonomial(self.get_expanded_tuple(), 
                                  self.get_coefficient())
        if temp_monomial.get_coefficient() == 0:
            return False
        elif temp_monomial.get_terms() == ():
            return True
        elif temp_monomial.first_square_index() == None:
            return True
        else:
            for index in xrange(temp_monomial.first_square_index(), 
                                len(temp_monomial.get_terms())-1):
                if type(temp_monomial.get_terms()[index+1][0]) == int:
                    if (temp_monomial.get_terms()[index][0] >= 
                        2 * temp_monomial.get_terms()[index+1][0]):
                        pass
                    else:
                        return False
                else:
                    return False
            return True

    def is_in(self, database):
        """
        This method standardizes the key format for all database files.
        """
        monomial_copy = self.copy()
        monomial_copy.collect_terms()
        return database.contains(monomial_copy.r_print())
        
    def is_left_module_form(self):
        """
        Checks if all "p" and "t" terms are on the left.
        """
        temp_monomial = RMonomial(self.get_expanded_tuple(), 
                                  self.get_coefficient())
        if temp_monomial.first_square_index() != None:
            for index in xrange(temp_monomial.first_square_index(), 
                                len(temp_monomial.get_terms())-1):
                if type(temp_monomial.get_terms()[index+1][0]) == int:
                    pass
                else:
                    return False
            return True
        else:
            return True

    def move_var_left(self, var, options):
        """
        Moves all the terms of type var to the left
        """
        temp_tuple = self.get_expanded_terms()
        number = len( [ x for x in temp_tuple if x == var ] )
        self.tuple_of_terms = tuple([ pair for pair in 
                                      self.get_terms() if pair[0] != 
                                      var ])
        if number:
            self.tuple_of_terms = (((var, number),) + 
                                   self.tuple_of_terms)

    def move_rhos_left(self, options):
        """
        Moves all the terms of type p to the left. (t should be "t", p
        should be "p").
        """
        self.move_var_left(options.get_p(), options)

    def move_taus_left(self, options):
        """
        Moves all the terms of type t to the left. (t should be "t", p
        should be "p").
        """
        self.move_var_left(options.get_t(), options)

    def move_u_left(self, options):
        self.move_var_left(options.get_u(), options)
    
    def rightmost_sq_tau_index(self, options):
        """
        returns the integer corresponding to the position of the
        rightmost tau object appearing in the monomial which has a Sq
        object directly to its left.
        """
        for index in xrange(1, len(self.get_terms())):
            if (self.get_terms()[-index][0] == options.get_t() and 
                type(self.get_terms()[-index-1][0]) == int):
                return len(self.get_terms())-index
            else:
                pass
        return None

    def rightmost_non_admissible_index(self, options):
        """
        returns index i for the most index pair (i-1, i) for
        which the pair of terms in these positions is
        non-admissible. An adem relation can be applied to this pair. 
        """
        if self.is_admissible():
            return None
        else:
            for index in xrange(1, len(self.get_terms())):
                if (type(self.get_terms()[-index][0]) == int and 
                    type(self.get_terms()[-index-1][0] == int)):
                    if (2 * self.get_terms()[-index][0] > 
                        self.get_terms()[-index-1][0]):
                        return len(self.get_terms())-index
                    else:
                        pass
                else:
                    pass
            return None
                                
    def strip_tau_rho(self, options):
        """
        updates the object to no longer have any instances of tau or
        rho. 
        also u!
        """
        temp_tuple = tuple([ term for term in self.get_terms() if 
                             (term[0] != options.get_t() and 
                              term[0] != options.get_p() and
                              term[0] != options.get_u()) ])
        self.tuple_of_terms = temp_tuple

    def strip_rho(self, options):
        """
        updates the object to no longer have any instances of tau or
        rho. 
        """
        temp_tuple = tuple([ term for term in self.get_terms() if 
                             term[0] != options.get_p() ])
        self.tuple_of_terms = temp_tuple

    def strip_squares(self, options):
        temp_tuple = tuple([ term for term in self.get_terms() if 
                             (term[0] == options.get_t() or 
                              term[0] == options.get_p() or
                              term[0] == options.get_u()) ])
        self.tuple_of_terms = temp_tuple

    def kill_squares(self, options):
        dual_flag = self.is_dual(options)
        if dual_flag:
            self.make_standard(options)
        self.remove_square_zeros()
        self_copy = self.copy()
        self_copy.strip_squares(options)
        if self.get_terms() != self_copy.get_terms():
            self.coefficient = 0
        if dual_flag:
            self.make_dual(options)

    def strip_sq_geq_2(self, options):
        temp_tuple = tuple([ term for term in self.get_terms() if 
                             (term[0] == options.get_t() or 
                              term[0] == options.get_p()) or 
                             term[0] == 1])
        self.tuple_of_terms = temp_tuple

    def kill_sq_geq_2(self, options):
        self.remove_square_zeros()
        self_copy = self.copy()
        self_copy.strip_sq_geq_2(options)
        if self.get_terms() != self_copy.get_terms():
            self.coefficient = 0

    def has_sq_1(self, options):
        for pair in self.get_terms():
            if pair[0] == 1:
                return True
        return False

    def has_squares(self, options):
        for pair in self.get_terms():
            if type(pair[0]) == int and pair[0] > 0:
                return True
        return False

    def largest_submonomial_stored_bounds(self, database):
        """
        Returns the bounds of the largest submonomial which is stored
        in database. If no such submonomial is stored, returns None.

        Be very careful that you either have expanded the monomial
        before doing this, or have something particular in mind. For
        example, if t^2t^3 is your monomial, and { t^4:value } is
        database, this will report that no submonomial is
        stored. However, if your monomial is ttttt, it will pick up
        that a t^4 is stored. 
        """
        bounds_list = [ (i, j) for i in 
                        range(0, len(self.get_terms())) for j in 
                        range(0, len(self.get_terms())) if i < j ]
        bounds_list = sorted(bounds_list, key=lambda entry: 
                             entry[1] - entry[0])
        bounds_list.reverse()
        for bounds in bounds_list:
            if RMonomial( self.get_terms()[bounds[0]:bounds[1]+1], 
                          1).is_in(database):
                return bounds
            else:
                pass
        return None


def vector_addition(*args):
    """
    should call this tuple addition.
    
    args are just tuples of the same length

    will toss an error if they do not have the same length
    """
    out_dict = {}
    args = list(args)
    length = len(args[0])
    for i in xrange(length):
        out_dict[i] = 0
    while args:
        v = args.pop()
        if len(v) == length:
            for i in xrange(length):
                out_dict[i] = out_dict[i] + v[i]
        else:
            print "tuples not of same length"
            raise ValueError
    output =()
    for i in xrange(length):
        output += (out_dict[i],) 
    return output
        

def scalar_multiply(c, v):
    output = ()
    for x in v:
        output = output + (c*x, )
    return output

def degree_function(n):
    return (n, n/2)

