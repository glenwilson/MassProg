from r_polynomial import *
from r_monomial import *
from r_steenrod_algebra import *

def finite_odd_3_h_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,min(n+1, 2)) for y in range(0, m+1) ]:
        if pair[0] <= pair[1] :
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_p(), pair[0]), 
                           (options.get_t(), pair[1] - pair[0])),1))
            new_poly = RPolynomial((new_monomial,))
            new_poly.simplify(options)
            output[pair] = (new_poly,)
        else:
            output[pair] = ()
    return output

def finite_odd_3_h_dual(n, m, options):
    output = {}
    for pair in [(-x, -y) for x in range(0,min(n+1, 2)) \
                     for y in range(0, m+1) ]:
        if pair[0] >= pair[1]:
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_p_dual(), -pair[0]), 
                           (options.get_t_dual(), -pair[1] + pair[0] )), 1))
            new_poly = RPolynomial((new_monomial,))
            new_poly.simplify(options)
            output[pair] = (new_poly, )
        else:
            output[pair] = ()
    return output

def finite_odd_1_h_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,min(n+1, 2)) for y in range(0, m+1) ]:
        if pair[0] <= pair[1] :
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_u(), pair[0]), 
                           (options.get_t(), pair[1] - pair[0])), 1))
            new_poly = RPolynomial((new_monomial,))
            new_poly.simplify(options)
            output[pair] = (new_poly,)
        else:
            output[pair] = ()
    return output

def finite_odd_1_h_dual(n, m, options):
    output = {}
    for pair in [(-x, -y) for x in range(0,min(n+1, 2)) \
                     for y in range(0, m+1) ]:
        if pair[0] >= pair[1]:
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_u_dual(), -pair[0]), 
                           (options.get_t_dual(), -pair[1] + pair[0] )), 1))
            new_poly = RPolynomial((new_monomial,))
            new_poly.simplify(options)
            output[pair] = (new_poly, )
        else:
            output[pair] = ()
    return output


##This should be modified to interchange n and m! Hopefully not making
##big issues...
def real_h_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        print pair
        if pair[0] >= pair[1] :
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_p(), pair[1]), 
                           (options.get_t(), pair[0] - pair[1] )),1))
            new_poly = RPolynomial((new_monomial,))
            print new_poly
            new_poly.simplify(options)
            print new_poly
            output[pair] = (new_poly,)
        else:
            output[pair] = ()
    return output

def real_h_dual(n, m, options):
    output = {}
    for pair in [(-x, -y) for x in range(0,n+1) for y in range(0, m+1) ]:
        if pair[0] >= pair[1]:
            new_monomial = RMonomial((),1)
            new_monomial.right_multiply(
                RMonomial(((options.get_p_dual(), -pair[0]), 
                           (options.get_t_dual(), pair[0] - pair[1] )), 1))
            new_poly = RPolynomial((new_monomial,))
            new_poly.simplify(options)
            output[pair] = (new_poly, )
        else:
            output[pair] = ()
    return output

def complex_h_star(n, m, options):
    output = {}
    for pair in [(x, y) for x in range(0,n+1) for y in range(0, m+1) ]:
        if not pair[0]:
            new_monomial = RMonomial(((options.get_t(), pair[1]),), 1)
            new_poly = RPolynomial((new_monomial,))
            output[pair] = (new_poly,)
        else:
            output[pair] = ()
    return output

def complex_h_dual(n, m, options):
    output = {}
    for pair in [(-x, -y) for x in range(0,n+1) for y in range(0, m+1) ]:
        if not pair[0]:
            new_monomial = RMonomial(((options.get_t_dual(), -pair[1]),), 1)
            new_poly = RPolynomial((new_monomial,))
            output[pair] = (new_poly,)
        else:
            output[pair] = ()
    return output
    
def classical_h_star(n, m, options):
    output = {}
    output[(0,0)] = (RSq(),)
    return output

def classical_h_dual(n, m, options):
    output = {}
    output[(0,0)] = (RSq(),)
    return output

def h_star(n, m, options):
    if options.get_case() == "Real":
        return real_h_star(n, m, options)
    elif options.get_case() == "Complex":
        return complex_h_star(n, m, options)
    elif options.get_case() == "Classical":
        return classical_h_star(n, m, options)
    elif options.get_case() == "FiniteOdd3":
        return finite_odd_3_h_star(n, m, options)
    elif options.get_case() == "FiniteOdd1":
        return finite_odd_1_h_star(n, m, options)

def h_dual(n, m, options):
    if options.get_case() == "Real":
        return real_h_dual(n, m, options)
    elif options.get_case() == "Complex":
        return complex_h_dual(n, m, options)
    elif options.get_case() == "Classical":
        return classical_h_dual(n, m, options)
    elif options.get_case() == "FiniteOdd3":
        return finite_odd_3_h_dual(n, m, options)
    elif options.get_case() == "FiniteOdd1":
        return finite_odd_1_h_dual(n, m, options)
