from polynomial import Polynomial
from r_monomial import RMonomial
from stack_obj import StackObj

class RPolynomial(Polynomial):
    def get_degree(self, options):
        """
        Returns a tuple consisting of the degrees of each monomial for
        the polynomial.

        This will not work for general monomial objs, as they do not
        have get_degree method. ONly to be applied to instances. 
        """
        output = ()
        for monomial in self.get_monomial_tuple():
            output = output + (monomial.get_degree(options), )
        if output:
            return output
        else:
            return (0,0)

    def get_degree_pair(self, options):
        """
        Returns a tuple consisting of the degrees of each monomial for
        the polynomial.

        This will not work for general monomial objs, as they do not
        have get_degree method. ONly to be applied to instances. 
        """
        output = ()
        for monomial in self.get_monomial_tuple():
            output = output + (monomial.get_degree(options), )
        if output:
            for pair in output:
                if output[0] == pair:
                    pass
                else:
                    return output
            return output[0]
        else:
            return (0,0)

    def __str__(self):
        return self.r_print()

    def r_print(self):
        return self._print("Sq")
    
    def is_monomial(self):
        return len(self.get_monomial_tuple()) == 1

    def is_admissible(self):
        """
        Returns true if all monomials are admissible. False otherwise.
        """
        for monomial in self.get_monomial_tuple():
            if monomial.is_admissible():
                pass
            else:
                return False
        return True

    def case_modification(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.case_modification(options)

    def is_standard(self, options):
        for monomial in self.get_monomial_tuple():
            if not monomial.is_standard(options):
                return False
        return True

    def is_dual(self, options):
        for monomial in self.get_monomial_tuple():
            if not monomial.is_dual(options):
                return False
        return True

    def make_dual(self, options):
        if not self.is_standard(options):
            print str(self)
            raise TypeError("not in standard notation")
        new_tuple = ()
        for monomial in self.get_monomial_tuple():
            new_tuple = new_tuple + (monomial.get_dual(options),)
        self.tuple_of_monomials = new_tuple

    def get_dual(self, options):
        self_copy = self.copy()
        self_copy.make_dual(options)
        return self_copy

    def make_standard(self, options):
        if not self.is_dual(options):
            print str(self)
            raise TypeError("not in standard notation")
        new_tuple = ()
        for monomial in self.get_monomial_tuple():
            new_tuple = new_tuple + (monomial.get_standard(options),)
        self.tuple_of_monomials = new_tuple

    def get_standard(self, options):
        self_copy = self.copy()
        self_copy.make_standard(options)
        return self_copy

    def is_left_module_form(self):
        """
        Returns true if all monomials are in left module form. False
        otherwise.
        """
        for monomial in self.get_monomial_tuple():
            if monomial.is_left_module_form():
                pass
            else:
                return False
        return True

    def kill_squares(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.kill_squares(options)

    def kill_sq_geq_2(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.kill_sq_geq_2(options)

    def has_sq_1(self, options):
        if len(self.get_monomial_tuple()) > 1:
            raise TypeError
        else:
            monomial = self.get_monomial_tuple()[0]
            return monomial.has_sq_1(options)

    def has_squares(self, options):
        if len(self.get_monomial_tuple()) > 1:
            raise TypeError
        else:
            monomial = self.get_monomial_tuple()[0]
            return monomial.has_squares(options)

    def dualize(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.dualize(options)
            
    def get_dualized_polynomial(self, options):
        self_copy = self.copy()
        self_copy.dualize(options)
        return self_copy

    def is_in(self, database):
        """
        Argument is database object. 

        For LeftMod, keys in database are to be self.r_print of RPoly
        objects which contain only one monomial (so a monomial).
        
        For AdmissibleForm, keys should be self.r_print of RPoly
        monomials which contain no taus or rhos.
        """
        return database.contains(self.r_print())

    def move_rhos_left(self, options):
        """
        For each monomial, will move all rhos to the left of the
        monomial.
        """
        for monomial in self.get_monomial_tuple():
            monomial.move_rhos_left(options)

    def move_u_left(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.move_u_left(options)

    def strip_tau_rho(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.strip_tau_rho(options)
    
    def strip_rho(self, options):
        for monomial in self.get_monomial_tuple():
            monomial.strip_tau(options)

    def remove_square_zeros(self):
        for monomial in self.get_monomial_tuple():
            monomial.remove_square_zeros()

    def remove_squares(self):
        for monomial in self.get_monomial_tuple():
            monomial.remove_squares()

    def apply_relation_from_database(self, database):
        """
        for each monomial, looks if there are any stored relations in
        database which can be applied, and then applies them. 
        """
        temp_polynomial = RPolynomial(())
        for monomial in self.get_monomial_tuple():
            if monomial.largest_submonomial_stored_bounds(database):
                bounds = monomial.largest_submonomial_stored_bounds(
                    database)
                left_part = RPolynomial((RMonomial(
                            monomial.get_terms()[:bounds[0]],1),))
                right_part = RPolynomial((RMonomial( 
                            monomial.get_terms()[bounds[1]+1:],1),))
                submonomial = RPolynomial((RMonomial( 
                            monomial.get_terms()[bounds[0]:bounds[1]+1], 
                            1), ))
                submonomial.collect_terms()
                relation = database.read(
                    submonomial.r_print()).copy()
                relation.left_multiply(left_part)
                relation.right_multiply(right_part)
                temp_polynomial.add(relation)
            else:
                temp_polynomial.add(monomial)
        self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()

    def apply_basic_commutativity_relation(self, options):
        """
        Will move all rhos to the left, use an elementary
        commutativity relation. 
        """
        ###new stuff
        if options.get_case() == "Classical":
            self.case_modification(options)
            return
        elif options.get_case() == "Complex":
            self.case_modification(options)
            return
        elif options.get_case() == "FiniteOdd3":
            self.case_modification(options)
        ###
        self.move_rhos_left(options)
        self.move_u_left(options)
        self.combine_monomials()
        if self.is_left_module_form():
            pass
        else:
            temp_polynomial = RPolynomial(())
            for monomial in self.get_monomial_tuple():
                if monomial.is_left_module_form():
                    temp_polynomial.add(monomial)
                else:
                    monomial.expand_terms()
                    index = monomial.rightmost_sq_tau_index(options)
                    left_part = RPolynomial((
                            RMonomial(monomial.get_terms()[:index-1],1),))
                    right_part = RPolynomial((
                            RMonomial(monomial.get_terms()[index+1:],1),))
                    relation = basic_commutativity_relation(
                        monomial.get_terms()[index-1][0], options)
                    relation.left_multiply(left_part)
                    relation.right_multiply(right_part)
                    temp_polynomial.add(relation)
            self.tuple_of_monomials = temp_polynomial.tuple_of_monomials
            self.move_rhos_left(options)
            self.move_u_left(options)
            self.combine_monomials()

    def apply_commutativity_relation(self, options):
        """
        This will first try to apply the largest stored commutativity
        relation to each monomial. Failing that, it will apply a basic
        commutativity relation.
        """
        if self.is_left_module_form():
            self.move_rhos_left(options)
            self.move_u_left(options)
        else:
            temp_polynomial = RPolynomial(())
            for monomial in self.get_monomial_tuple():
                monomial.move_rhos_left(options)
                monomial.move_u_left(options)
                monomial.expand_terms()
                #potential room for improvement here by getting rid of
                #rhos where unnecessary
                if monomial.is_left_module_form():
                    temp_polynomial.add(monomial)
                elif monomial.largest_submonomial_stored_bounds(
                    options.get_comm_db()):
                    temp_summand = RPolynomial(monomial.copy())
                    temp_summand.apply_relation_from_database(
                        options.get_comm_db())
                    temp_summand.move_rhos_left(options)
                    temp_summand.move_u_left(options)
                    temp_polynomial.add(temp_summand)
                else:
                    temp_monomial = monomial.copy()
                    relation = RPolynomial(temp_monomial)
                    relation.apply_basic_commutativity_relation(options)
                    temp_polynomial.add(relation)
            self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()
            self.move_rhos_left(options)
            self.move_u_left(options)
            self.combine_monomials()
#new!
            self.case_modification(options)

    def storage_make_left_module_form(self, options):
        self.move_rhos_left(options)
        self.move_u_left(options)
        self.combine_monomials()
        while not self.is_left_module_form():
            self.apply_commutativity_relation(options)
            self.move_rhos_left(options)
            self.move_u_left(options)
            self.combine_monomials()
            self.case_modification(options)

    def left_module_form(self, options):
        """
        Will update the polynomial to one in which all rhos and taus
        are to the left of the Sqi's. 
        """
        ###
        if options.get_case() == "Classical":
            self.case_modification(options)
            return
        elif options.get_case() == "Complex":
            self.case_modification(options)
            return
        elif options.get_case() == "FiniteOdd3":
            self.case_modification(options)
        ###
        self.combine_monomials()
        stack = []
        for monomial in self.get_monomial_tuple():
            monomial_copy = monomial.copy()
            monomial_copy.strip_rho(options)
            if monomial_copy.is_left_module_form():
                pass
            else:
                stack.append( StackObj(RPolynomial(monomial_copy), 
                                       [RPolynomial(monomial_copy)], 
                                       RPolynomial(())) )
        while stack:
            entry = stack[-1]
            if entry.get_queue():
                last_term = entry.get_queue().pop()
                last_term_copy = last_term.copy()
                last_term_copy.apply_commutativity_relation(options)
                for summand in last_term_copy.get_monomial_tuple():
                    summand.move_rhos_left(options)
                    summand.move_u_left(options)
                    if summand.is_left_module_form():
                        entry.get_output().add(RPolynomial(summand))
                    else:
                        entry.get_queue().append(RPolynomial(summand))
                        summand_copy = summand.copy()
                        summand_copy.strip_rho(options)
                        stack.append(StackObj(RPolynomial(summand_copy),
                                              [RPolynomial(summand_copy)
                                               ], RPolynomial(())))
            else:
                entry_term = entry.get_monomial().copy()
                entry_term.collect_terms()
                output_polynomial = entry.get_output().copy()
                output_polynomial.move_rhos_left(options)
                output_polynomial.move_u_left(options)
                output_polynomial.combine_monomials()
                options.get_comm_db().write(entry_term.r_print(), 
                                             output_polynomial.copy())
                stack.pop()
        self.storage_make_left_module_form(options)

    def apply_adem_relation(self, options):
        """
        Will apply the rightmost adem relation possible to each monomial. 

        Practical usage notes: If your polynomial is not in left
        module form, this might not do much! This method does not put
        the monomial into left module form.

        To make life easier on the algorithm, it will first reduce the
        polynomial mod 2.
        """
        self.combine_monomials()
        self.case_modification(options)
        temp_polynomial = RPolynomial(())
        for monomial in self.get_monomial_tuple():
            monomial.expand_terms()
            if type(monomial.rightmost_non_admissible_index(options)) == int:
                index = monomial.rightmost_non_admissible_index(options)
                left_part = RPolynomial((
                        RMonomial(monomial.get_terms()[:index-1],1),))
                right_part = RPolynomial((
                        RMonomial(monomial.get_terms()[index+1:],1),))
                relation = adem_relation(
                    monomial.get_terms()[index-1][0], 
                    monomial.get_terms()[index][0], options)
                relation.left_multiply(left_part)
                relation.right_multiply(right_part)
                temp_polynomial.add(relation)
            else:
                temp_polynomial.add(monomial)
        self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()
        self.remove_square_zeros()
        ###
        self.case_modification(options)
        ###
        self.combine_monomials()


    def apply_admissible_relation(self, options):
        """
        For each monomial in the polynomial, this will apply a
        relation from storage if it exists, or will apply an adem
        relation. 

        If monomials not in left module form, this might not do much!
        """
        self.case_modification(options)
        if self.is_admissible():
            pass
        else:
            temp_polynomial = RPolynomial(())
            for monomial in self.get_monomial_tuple():
                monomial.expand_terms()
                if monomial.is_admissible():
                    temp_polynomial.add(monomial)
                elif monomial.largest_submonomial_stored_bounds(
                    options.get_adem_db()):
                    temp_summand = RPolynomial(monomial.copy())
                    temp_summand.apply_relation_from_database(
                        options.get_adem_db())
                    temp_polynomial.add(temp_summand)
                else:
                    temp_monomial = monomial.copy()
                    relation = RPolynomial(temp_monomial)
                    relation.apply_adem_relation(options)
                    temp_polynomial.add(relation)
            self.tuple_of_monomials = temp_polynomial.get_monomial_tuple()
            self.remove_square_zeros()
            self.combine_monomials()
            self.case_modification(options)

    def storage_simplify(self, options):
        """
        Will update the polynomial to be expressed in terms of the
        basis of admissible monomials.
        """
        while not self.is_admissible():
            self.apply_admissible_relation(options)
            self.left_module_form(options)
            
    def standard_simplify(self, options):
        """
        Will update the polynomial to be expressed in terms of the
        basis of admissible monomials.
        
        This used to be just simplify!
        """
        self.combine_monomials()
        self.case_modification(options)
        self.left_module_form(options)
        stack = []
        for monomial in self.get_monomial_tuple():
            monomial_copy = monomial.copy()
            monomial_copy.strip_tau_rho(options)
            if monomial_copy.is_admissible():
                pass
            else:
                stack.append(StackObj(RPolynomial(monomial_copy), 
                                      [RPolynomial(monomial_copy)], 
                                      RPolynomial(())))
        while stack:
            entry = stack[-1]
            if entry.get_queue():
                last_term = entry.get_queue().pop()
                last_term_copy = last_term.copy()
                last_term_copy.left_module_form(options)
                last_term_copy.expand_terms()
                last_term_copy.apply_admissible_relation(options)
                last_term_copy.left_module_form(options)
                for a_monomial in last_term_copy.get_monomial_tuple():
                    summand = RPolynomial(a_monomial)
                    for summand_monomial in summand.get_monomial_tuple():
                        if summand_monomial.is_admissible():
                            entry.get_output().add(
                                RPolynomial(summand_monomial))
                        else:
                            entry.get_queue().append(
                                RPolynomial(summand_monomial))
                            summand_monomial_copy = summand_monomial.copy()
                            summand_monomial_copy.strip_tau_rho(options)
                            stack.append(StackObj(
                                    RPolynomial(summand_monomial_copy),
                                    [RPolynomial(summand_monomial_copy)],
                                    RPolynomial(())))
            else:
                entry_term = entry.get_monomial().copy()
                entry_term.collect_terms()
                output_polynomial = entry.get_output().copy()
                output_polynomial.remove_square_zeros()
                output_polynomial.left_module_form(options)
                options.get_adem_db().write(entry_term.r_print(), 
                                    output_polynomial.copy())
                stack.pop()
        self.storage_simplify(options)
        self.case_modification(options)

    def dual_simplify(self, options):
        if not self.is_dual(options):
            print self
            raise TypeError("not in dual notation")
        self.make_standard(options)
        self.simplify(options)
        self.make_dual(options)

    def simplify(self, options):
        if self.is_standard(options):
            self.standard_simplify(options)
        elif self.is_dual(options):
            self.dual_simplify(options)
        else:
            print self
            raise TypeError("neither dual nor standard notation!")


def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def basic_commutativity_relation(n, options):
    """
    Given integer n, generator names t and p (should be string "t" and
    "p" respectively), will return the RPolynomial equal to "Sqn*t".
    """
    if n == 0:
        #this should never happen
        return RPolynomial(RMonomial(((options.get_t(),1),),1))
    elif n == 1:
        return RPolynomial((RMonomial(((options.get_t(),1),(1,1)),1), 
                            RMonomial(((options.get_p(),1),),1)))
    elif n % 2 == 0:
        return RPolynomial((RMonomial(((options.get_t(),1),(n,1)),1), 
                            RMonomial(((options.get_p(),1),(options.get_t(),1),(n-1,1)),1)))
    elif n % 2 == 1:
        return RPolynomial((RMonomial(((options.get_t(),1),(n,1)),1), 
                            RMonomial(((options.get_p(),1),(n-1,1)),1), 
                            RMonomial(((options.get_p(),2),(n-2,1)),1)))

def adem_relation(a, b, options):
    """
    This returns an RPolynomial which is equal to Sqa*Sqb. The formula
    is given by the motivic adem relations. The optional arguments p
    and t represent the string corresponding to tau and rho
    resepectively.
    """
    out = RPolynomial(())
    if a <= 0 or b <= 0 or a >= 2*b:
        return out
    elif a % 2 == 1 and b % 2 == 1:
        for k in range(0, (a / 2) + 1):
            out.add(RMonomial(((a+b-k,1),(k,1)), choose(b-1-k, a-2*k)))
        return out
    elif a % 2 == 0 and b % 2 == 0:
        for k in range(0, (a/2) + 1):
            if k % 2:
                out.add(RMonomial(((options.get_t(), 1),(a+b-k,1),(k,1)), 
                              choose(b-k-1, a-2*k)))
            else:
                out.add(RMonomial(((a+b-k,1),(k,1)), choose(b-k-1, a-2*k)))
        return out
    elif a % 2 == 0 and b % 2 == 1:
        for k in range(0, (a/2) + 1):
            out.add(RMonomial(((a+b-k,1),(k,1)),choose(b-1-k,a-2*k)))
            if k % 2:
                out.add(RMonomial(((options.get_p(),1),(a+b-k-1,1),(k,1)), 
                                  choose(b-1-k,a-2*k)))
            else:
                pass
        return out
    elif a % 2 == 1 and b % 2 == 0:
        for k in range(0, (a/2) + 1):
            if k % 2:
                out.add(RMonomial(((options.get_p(),1),(a+b-1-k,1),(k,1)), 
                                  choose(b-1-k, a-1-2*k)))
            else:
                out.add(RMonomial(((a+b-k,1),(k,1)), 
                                  choose(b-1-k,a-1-2*k)))
        return out

    

