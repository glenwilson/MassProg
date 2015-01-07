# requires BitVector
from bit_vector import BitVector

# for shallow/deep copies
import copy

# for random matrices
import random

class BitMatrix(object):
   '''
   Return an identity matrix
   '''
   @staticmethod
   def identity_matrix(size):
      rows = []
      for i in xrange(size):
         row = BitVector(size)
         row[i] = 1
         rows.append(row);

      return rows

   @staticmethod
   def get_blank_matrix( num_row, num_column ):
      rows = []
      for i in xrange( num_row ):
         row = BitVector( num_column )
         rows.append( row )

      return BitMatrix(rows)

   @staticmethod
   def get_random_matrix( num_row, num_column ):
      random_matrix = BitMatrix.get_blank_matrix(num_row, num_column)
      entry_count = (int)(num_row * num_column)
      num_ones = (int) (random.random() * entry_count )
      random_entries = random.sample( xrange(entry_count), num_ones )
      for index in random_entries:
         i = (int)(index/num_column )
         j = index % num_column
         random_matrix.set_entry(i, j)

      return random_matrix

   def __init__(self, row_array):
      self._rows = row_array
      self._row_count = len(row_array)
      self._col_count = 0
      if row_array:
         self._col_count = len(row_array[0])
         for row in row_array:
            if len(row) != self._col_count:
               print self._col_count
               print len(row)
               raise TypeError("length of rows is inconsistent")

      self.basis_change = BitMatrix.identity_matrix(self._row_count)
      self.basis_change_flag = False

      self._rref = []
      self._rref_flag = False
      self.row_weights = []
      self.row_weights_flag = False

   '''
   Properties accessors
   '''
   def get_matrix(self):
      matrix = []
      for i in xrange(self.get_row_count()):
         matrix.append( self.get_row(i) )
      return matrix

   def get_row(self, i):
      return self._rows[i].copy()

   def get_column(self, j):
      col = BitVector(self.get_row_count())
      for i in xrange(self.get_row_count()):
         col[i] = self.get_entry(i, j)
      return col

   def get_entry(self, i, j):
      return self._rows[i][j]

   def get_row_count(self):
      return self._row_count

   def get_col_count(self):
      return self._col_count

   def get_size(self):
      return (self.get_row_count(), self.get_col_count())

   def get_rank(self):
      rank = 0
      for row in self.get_rref():
         if not row.is_zero():
            rank += 1
      return rank

   def copy(self):
      return copy.deepcopy(self)

   def get_basis_change(self):
      if not self.basis_change_flag:
         self.compute_rref()
      return BitMatrix(self.basis_change)

   def is_zero(self):
      for row in self._get_matrix():
         if not row.is_zero():
            return False
      return True

   def can_solve(self, vector):
      """
      This assumes the input is a bit vector
      """
      reduced_vector = self.get_basis_change() * vector
      for index in xrange( self.get_row_count() ):
         if not self.get_row_weights()[index] and reduced_vector[index]:
            return False
      return True

   def solve(self, vector):
      """
      vector is a bitvector
      """
      if not self.can_solve(vector):
         return False
      solution = BitVector(self.get_col_count())
      reduced_vector = self.get_basis_change() * vector
      rref = self.get_rref()
      for index in range(0, self.get_row_count()):
         solution[rref[index].get_leading_index()] = \
             reduced_vector[index]
      return solution
         
   def all_solutions(self, vector):
      """
      denote the matrix as A, and the vector as b
      vector is a bitvector

      returns a set of all solutions to Ax=b
      If there are no solutions, returns False
      """
      out_set = set()
      ker = self.get_kernel()
      xx = self.solve(vector)
      if not xx:
         return False
      coeffs = BitVector.vector_space_set(len(ker))
      for cc in coeffs:
         new = xx.copy()
         for i in range(0,len(ker)):
            if cc[i]:
               new += ker[i]
         out_set.add(new)
      return out_set

   def complement_row_space(self):
      leading_term_list = [ row.get_leading_index() for row
         in self.get_rref() if not row.is_zero() ]
      free_variables = [ index for index in xrange( self._col_count ) 
         if index not in leading_term_list ]
      complement = []
      for index in free_variables:
         ee = BitVector(self.get_col_count())
         ee[index] = 1
         complement.append(ee)
      return complement

   '''
   Operations
   '''
   def __mul__(self, other):
      if isinstance( other, BitVector ):
         output = BitVector( self._row_count ) 
         # output = BitMatrix.get_blank_matrix( self._row_count, 1 )
         for i in xrange( self._row_count ):
            output[i] = (bool) (self._rows[i] * other)
            # output.set_entry(i, 0, (bool) (self._rows[i] * other) )
         return output

      if not self._col_count == other._row_count:
         raise TypeError
      product_matrix = \
         BitMatrix.get_blank_matrix( self._row_count, other._col_count )

      for i in xrange( len( self._rows ) ):
         for j in xrange( other._col_count ):
            product_matrix.set_entry(i, j,
               (bool)(self._rows[i] * other.get_column(j)) )
      return product_matrix

   def __add__(self, other):
      if (self._row_count != other._row_count) and (self._col_count != other._col_count):
         raise TypeError
      
      matrix_sum = []
      for index in range(0, self._row_count):
         matrix_sum.append(self.get_row(index) + other.get_row(index))
      output = BitMatrix(matrix_sum)
      return output
      

   '''
   Shallow accessors
   '''
   def _get_matrix(self):
      return self._rows

   def _get_row(self, i):
      return self._rows[i]

   '''
   Mutators!
   '''
   def reset_flags(self):
      self.basis_change_flag = False
      self.rref_flag = False
      self.row_weights_flag = False

   def set_entry(self, i, j, value = True):
      self._rows[i][j] = value

   def transpose(self):
      new_rows = []
      for i in xrange(self.get_col_count()):
         new_rows.append(self.get_column(i))
      self._rows = new_rows
      self._col_count = self._row_count
      self._row_count = len( new_rows )
      self.basis_change = BitMatrix.identity_matrix(self._row_count)
      self.reset_flags()

   def get_append_columns(self, vect_list):
      """ 
      vect_list is a list of bit_vectors which will be appended to the
      matrix as columns!!! not as rows. 

      this will be slow on large matrices! 
      """
      self_copy = self.copy()
      self_copy.transpose()
      new_rows = self_copy._rows
      for vect in vect_list:
         new_rows.append(vect)
      new_mat = BitMatrix(new_rows)
      new_mat.transpose()
      return new_mat

   def swap_rows(self, i, j):
      row_temp = self._rref[j]
      self._rref[j] = self._rref[i]
      self._rref[i] = row_temp

      row_temp = self.basis_change[j]
      self.basis_change[j] = self.basis_change[i]
      self.basis_change[i] = row_temp

   def add_row(self, i, j):
      self._rref[j] = self._rref[j] + self._rref[i]
      self.basis_change[j] += self.basis_change[i]

   def get_rref(self):
      if not self._rref_flag:        
         self.compute_rref()
      return self._rref

   def compute_rref(self):
      if self._rref_flag and self.basis_change_flag:
         return
      self._rref = rows = copy.copy(self._rows)
      col_count = self._col_count
      row_count = self._row_count
      current_index = 0
      for i in xrange(col_count):
         if current_index >= self._row_count:
            break
         current_row = rows[current_index]
         if current_row[i] == 0:
            has_swapped = False
            for j in range(current_index + 1, row_count):
               if rows[j][i] == 1:
                  self.swap_rows(current_index, j)
                  has_swapped = True
                  break
            #current_index += 1 if has_swapped else 0
            if not has_swapped:
               continue
         # start cancelling things
         for j in range(current_index + 1, row_count):
            if rows[j][i] == 1:
               self.add_row( current_index, j)
         for j in range(0, current_index):
            if rows[j][i] == 1:
               self.add_row( current_index, j)
         current_index += 1
      self._rref_flag = True
      self.basis_change_flag = True

   def get_kernel(self):
      leading_term_list = [ row.get_leading_index() for row
         in self.get_rref() if not row.is_zero() ]
      free_variables = [ index for index in 
         xrange( self._col_count ) 
         if index not in leading_term_list ]
      kernel = []

      for column_index in free_variables:
         current_vector = BitVector( self._col_count )
         for row in self.get_rref():
            if not row.is_zero():
               leading_term = row.get_leading_index()
               if row[column_index] == 1:
                  current_vector[leading_term] = 1
         current_vector[column_index] = 1
         kernel.append( current_vector )
      return kernel

   def compute_row_weights(self):
      if self.row_weights_flag:
         return
      rref = self.get_rref()
      self.row_weights = BitVector(self.get_row_count())
      for index in xrange(self.get_row_count()):
         if not rref[index].is_zero():
            self.row_weights[index] = 1
      self.row_weights_flag = True

   def get_row_weights(self):
      if not self.row_weights_flag:
         self.compute_row_weights()
      return self.row_weights

   def get_inverse(self):
      #check if square matrix
      if self.get_row_count() != self.get_col_count():
         return False 
      #check if full rank
      if self.get_rank() != self.get_row_count():
         return False
      #solve e_i = Ax for all i
      out_columns = []
      for i in range(self.get_row_count()):
         ee = BitVector(self.get_rank())
         ee[i] = 1
         xx = self.solve(ee)
         out_columns.append(xx)
      #assemble x_i into matrix 
      out_matrix = BitMatrix(out_columns)
      out_matrix.transpose()
      return out_matrix

      
   def __str__(self):
      rows = map( lambda x: x.__str__(), self._rows )
      self_str = '\n'.join(rows)
      return self_str

   '''
   Pickling
   '''
   def __getstate__(self):
      return { 'rows'              : self._rows,
               'basis_change'      : self.basis_change,
               'basis_change_flag' : self.basis_change_flag,
               'rref'              : self._rref,
               'rref_flag'         : self._rref_flag,
               'row_weights'       : self.row_weights,
               'row_weights_flag'  : self.row_weights_flag, 
               '_row_count'        : self._row_count,
               '_col_count'        : self._col_count}

   def __setstate__(self, _dict):
      self._rows = _dict['rows']
      self.basis_change = _dict['basis_change']
      self.basis_change_flag = _dict['basis_change_flag']
      self._rref = _dict['rref']
      self._rref_flag = _dict['rref_flag']
      self.row_weights = _dict['row_weights']
      self.row_weights_flag = _dict['row_weights_flag']
      self._row_count = _dict['_row_count']
      self._col_count = _dict['_col_count']
