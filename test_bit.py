from bit_vector import BitVector
from bit_matrix import BitMatrix 
from cohomology import Cohomology

# A = BitMatrix.get_random_matrix(3,3)
# B = A.get_inverse()

# print "matrix A"
# print A
# print "the inverse"
# print B 
# print "the product"
# print A * B

B = BitMatrix.get_random_matrix(20,10)
A = BitMatrix.get_blank_matrix(10,2)
print "the matrix B"
print B
print "the matrix A"
print A
print "the kernel"
for thing in B.get_kernel():
    print thing

cohom = Cohomology(B, A)
C = BitMatrix(cohom.get_extended_ker_basis())
C.transpose()
print "now the extended basis"
print C
print "testing invertibility"
print C * cohom.basis_to_ker_basis()
