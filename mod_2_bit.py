
class MatrixFactory:
   @staticmethod
   def mod_2_to_bit_matrix( mod2mat ):
      rows = []
      for i in xrange( mod2mat.get_size()[0] ):
         rows.append( VectorFactory.mod_2_to_bit_vector( mod2mat.get_row(i) ) )
      return BitMatrix( rows )

class VectorFactory:
   def mod_2_to_bit_vector( mod2vect ):
