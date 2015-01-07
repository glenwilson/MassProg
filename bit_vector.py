import cPickle as pickle
import array
import copy
import string
import random

class DimensionException(Exception):
   def __str__(self):
      return "Dimension mismatch"

class BitVector(object):
   @staticmethod
   def vector_space_set(k):
      """
      returns the set of all vectors in k-space
      """
      out = set()
      out.add(BitVector(k))
      for i in range(0,k):
         temp = out.copy()
         for vector in temp:
            copy = vector.copy()
            copy[i] = 1
            out.add(copy)
      return out

   @staticmethod
   def random_vector(length):
      """
      returns random vector of given length
      """
      x = BitVector(length)
      for index in xrange(length):
         x[index] = random.randint(0,1)
      return x

   def __init__(self, len):
      self.bit_vector = array.array('I', 
         (0 for i in xrange((len >> 5) + 1)))
      self.length = len

   def __add__(self, other):
      if self.length != other.length:
         raise DimensionException

      vector_sum = BitVector( self.length )
      vector = []
      for index in xrange(len(self.bit_vector)):
         vector.append( self.bit_vector[index] ^ other.bit_vector[index] )
      
      vector_sum.bit_vector = vector 
      return vector_sum
   
   def __mul__(self, other):
      if self.length != other.length:
         print self
         print other
         raise DimensionException

      dot_product = 0
      for index, item in enumerate(self.bit_vector):
         dot_product ^= (bin(item & other.bit_vector[index]).count('1'))

      return (dot_product & 1)

   def get_length(self):
      length = 0
      for item in enumerate(self.bit_vector):
         length += bin(item).count('1')

      return (length & 1)

   def scale(self, value):
      if not value: return BitVector(self.length)

      return self.copy()

   def copy(self):
      return copy.deepcopy(self)

   def number_of_components(self):
      counter = 0
      for index, item in enumerate(self.bit_vector):
         counter += (bin(item).count('1'))
      return counter

   def get_leading_index( self ):
      inclement = 0
      for num in self.bit_vector:
         current_index = bin(num)[::-1].find('1')
         if current_index != -1:
            return current_index + inclement

         inclement += 32
      return -1

   def __getitem__(self, position):
      if position >= self.length or position < 0:
         return 0

      vector_index = position >> 5
      return (self.bit_vector[vector_index] >> (position & 31)) & 1

   def __str__(self):
      last_index = self.length >> 5
      if last_index << 5 == self.length:
         last_index -= 1

      last_length = self.length & 31
      string_array = []
      for i in range(0, last_index + 1):
         word = bin(self.bit_vector[i])[2:]
         current_word_length = len(word)
         total_word_length = 32 if i < last_index else last_length
         padding_length = total_word_length - current_word_length
         padding = ''.join( '0' for j in xrange( padding_length ) )
         word_rep = string.join([padding, word], '')
         string_array.append( word_rep )

      string_array.reverse()
      return string.join( string_array , '')[::-1]

   def __len__(self):
      return self.length

   def is_zero(self):
      for num in self.bit_vector:
         if num != 0:
            return False
      return True

   ''' 
   Pickling functions
   '''
   def __getstate__(self):
      return { 'bit_vector'      : self.bit_vector, 
               'length'          : self.length }

   def __setstate__(self, _dict):
      self.bit_vector = _dict['bit_vector']
      self.length = _dict['length']

   ''' 
   @warning: Mutator!
   '''
   def __setitem__(self, position, value = True):
      if position >= self.length or position < 0:
         return

      vector_index = position >> 5
      bit_value = (1 if value else 0) << (position & 31)

      self.bit_vector[vector_index] |= bit_value
      self.bit_vector[vector_index] &= (((1 << 32) - 1) << (position + 1)) | \
                                       bit_value | \
                                       ((1 << position) - 1)

   def _set_vector(self, bit_vector):
      self.bit_vector = bit_vector

   def __iadd__(self, other):
      if self.length != other.length:
         raise DimensionException

      for index in xrange(len(self.bit_vector)):
         self.bit_vector[index] ^= other.bit_vector[index]

      return self
