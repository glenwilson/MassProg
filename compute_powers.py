from SteenrodAlg import * 

def produce_tuple(n, length):
    output = ()
    for i in range(0, length):
        output = output + (n, )
    return output

def compute_powers(n, filename, upper_bound=100):
    out_file = open(filename, 'a')
    for length in xrange(1, upper_bound):
        output_string = SteenrodSq(SqMonomial(produce_tuple(n, length))).stack_simplify().pretty_print()
        out_file.write("Sq" + str(n) + "^" + str(length) +  ": " + output_string + '\n')
        if output_string == "":
            break
        else:
            pass

for k in range(1,20):
    compute_powers(k, "out.txt")

