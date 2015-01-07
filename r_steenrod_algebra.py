from r_polynomial import *
from r_monomial import *

def RSq(*args):
    output = RMonomial((),1)
    for term in args:
        output.right_multiply(RMonomial(((term, 1),),1))
    return RPolynomial((output,))

def RPoly(*args):
    """
    input is 
    """
    output = tup(args)
    return RPolynomial(output)

def RSqTuple(a_tuple):
    output = RMonomial((),1)
    for term in a_tuple:
        output.right_multiply(RMonomial(((term, 1),),1))
    return RPolynomial((output,))
