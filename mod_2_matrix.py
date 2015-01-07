import copy
import random
from vector_space import ModTwoVectorSpace

class ModTwoMatrix(object):
    def __init__(self, matrix_list):
        self.matrix_list = matrix_list
        if matrix_list:
            for row in matrix_list:
                if len(row) == len(matrix_list[0]):
                    pass
                else:
                    raise TypeError
        self.reduce_mod_2()
        self.basis_change = None
        self.basis_change_flag = False
        self.rref = None
        self.rref_flag = False
        self.row_weights = []
        self.row_weights_flag = False

    def reset_flags(self):
        self.basis_change_flag = False
        self.rref_flag = False
        self.row_weights_flag = False

    def __getstate__(self):
        return {'matrix_list' : self.matrix_list,
                'basis_change' : self.basis_change,
                'basis_change_flag' : self.basis_change_flag,
                'rref' : self.rref,
                'rref_flag' : self.rref_flag,
                'row_weights' : self.row_weights,
                'row_weights_flag' : self.row_weights_flag}

    def __setstate__(self, _dict):
        self.matrix_list = _dict['matrix_list']
        self.basis_change = _dict['basis_change']
        self.basis_change_flag = _dict['basis_change_flag']
        self.rref = _dict['rref']
        self.rref_flag = _dict['rref_flag']
        self.row_weights = _dict['row_weights']
        self.row_weights_flag = _dict['row_weights_flag']

    def get_entry(self, i, j):
        return self.get_matrix()[i][j]
        
    def get_size(self):
        if len(self.get_matrix()):
            return (len(self.get_matrix()), len(self.get_matrix()[0]))
        else:
            return (0,0)

    def get_matrix(self):
        return self.matrix_list

    def get_row(self, i):
        return self.get_matrix()[i]

    def get_column(self, j):
        return [ self.get_entry(i, j) for i in range(0, self.get_size()[0])]

    def transpose(self):
        new_matrix = []
        for index in range(0,self.get_size()[1]):
            new_matrix.append(self.get_column(index))
        self.matrix_list = new_matrix
        self.reset_flags()

    def reduce_mod_2(self):
        new_matrix = []
        for row in self.matrix_list:
            new_row = []
            for entry in row:
                new_row.append(entry % 2)
            new_matrix.append(new_row)
        self.matrix_list = new_matrix
        self.reset_flags()

    def is_zero(self):
        self.reduce_mod_2()
        for row in self.get_matrix():
            for entry in row:
                if entry != 0:
                    return False
        return True
                    
    def add(self, other):
        if self.get_size() == other.get_size():
            output_matrix = []
            for index_i in range(0, self.get_size()[0]):
                new_row = []
                for index_j in range(0, self.get_size()[1]):
                    new_row.append( (self.get_matrix()[index_i][index_j] + 
                                     other.get_matrix()[index_i][index_j]) % 2 )
                output_matrix.append(new_row)
            self.matrix_list = output_matrix
        else: 
            raise TypeError("Matrices are wrong size")
        self.reduce_mod_2()
        self.reset_flags()

    def copy(self):
        """
        Now just a shallow copy instead of a deep copy.
        """
        return copy.deepcopy(self)

    def __add__(self, other):
        self_copy = self.copy()
        other_copy = other.copy()
        self_copy.add(other_copy)
        return self_copy

    def right_multiply(self, other):
        if self.get_size()[1] == other.get_size()[0]:
            new_matrix = []
            for index_i in range(0, self.get_size()[0]):
                new_row = []
                for index_j in range(0, other.get_size()[1]):
                    new_entry = 0
                    for index in range(0, self.get_size()[1]):
                        new_entry = new_entry + (self.get_entry(index_i, index) * 
                                              other.get_entry(index, index_j))
                    new_row.append(new_entry)
                new_matrix.append(new_row)
            self.matrix_list = new_matrix
        else:
            raise TypeError("Matrices are wrong size")
        self.reduce_mod_2()
        self.reset_flags()

    def left_multiply(self, other):
        new_matrix = other * self
        self.matrix_list = new_matrix.get_matrix()
        self.reset_flags()

    def __mul__(self, other):
        self_copy = self.copy()
        other_copy = other.copy()
        self_copy.right_multiply(other_copy)
        return self_copy

    def __str__(self):
        matrix_string = ""
        for row in self.get_matrix():
            for entry in row:
                matrix_string = matrix_string + str(entry) 
            matrix_string = matrix_string + "\n"
        return matrix_string[:-1]
    
    def add_row(self, i, j):
        """
        adds row i to row j, replacing row j with the result. 
        Row numbers start with 0.
        """
        row_i = self.get_matrix()[i]
        row_j = self.get_matrix()[j]
        new_row = []
        for index in range(0, len(row_i)):
            new_row.append(row_i[index] + row_j[index])
        self.matrix_list.pop(j)
        self.matrix_list.insert(j, new_row)
        self.reduce_mod_2()
        self.reset_flags()

    def append_matrix(self, matrix):
        if self.get_size()[0] != matrix.get_size()[0]:
            raise TypeError
        new_matrix = []
        for i in range(0, self.get_size()[0]):
            new_row = self.get_row(i)
            new_row = new_row + matrix.get_row(i)
            new_matrix.append(new_row)
        self.matrix_list = new_matrix
        self.reset_flags()
        
    def row_reduce(self, column_limit = 0):
        """
        Seems to work. will double check.
        """
        if column_limit == 0:
            column_limit = self.get_size()[1]
        counter = 0
        for index_j in range(0, column_limit):
            if counter < self.get_size()[0]:
#                print "next column"
#                print self
                if self.get_column(index_j)[counter:].count(0) == (self.get_size()[0] - counter):
                    pass
                else:
                    index_i = min([x for x in range(counter, self.get_size()[0]) if self.get_entry(x, index_j)])
 #                   print "index_i " + str(index_i)
                    if index_i == counter:
                        counter = counter + 1
                    else:
                        self.add_row(index_i, counter)
                        counter = counter + 1
 #                   print str(self)
                    for index_k in range(0, counter-1):
                        if self.get_entry(index_k, index_j):
                            self.add_row(counter - 1, index_k)
 #                           print self
                        else:
                            pass
                for index_k in range(counter, self.get_size()[0]):
                    if self.get_entry(index_k, index_j):
                        self.add_row(counter - 1, index_k)
 #                       print self
                    else:
                        pass
            else:
                pass
        self.reset_flags()

    # def get_row_reduced_matrix(self, column_limit = 0):
    #     self_copy = self.copy()
    #     self_copy.row_reduce(column_limit)
    #     return self_copy

    def get_submatrix(self, ul_corner, size):
        new_matrix = []
        for i in range(ul_corner[0], ul_corner[0] + size[0]):
            new_row = []
            for j in range(ul_corner[1], ul_corner[1] + size[1]):
                new_row.append(self.get_entry(i, j))
            new_matrix.append(new_row)
        return ModTwoMatrix(new_matrix)

    def compute_basis_change(self):
        self_copy = self.copy()
        original_size = self_copy.get_size()
        col_limit = self_copy.get_size()[1]
        id_matrix = identity_matrix( (self_copy.get_size()[0], 
                                      self_copy.get_size()[0]))
        self_copy.append_matrix(id_matrix)
        self_copy.row_reduce(col_limit)
        self.basis_change = self_copy.get_submatrix(
            (0, col_limit), (self_copy.get_size()[0], 
                             self_copy.get_size()[0]))
        self.basis_change_flag = True

    def compute_rref(self):
        self_copy = self.copy()
        self_copy.row_reduce()
        self.rref = self_copy
        self.rref_flag = True

    def get_rref(self):
        if not self.rref_flag:
            self.compute_rref()
        return self.rref 

    def compute_row_weights(self):
#        print "  In compute_row_weights"
#        print self.row_weights_flag
        if not self.row_weights_flag:
            for row in self.get_rref().get_matrix():
                weight = 0
                for entry in row:
                    weight = weight + entry
                self.row_weights.append(weight)
            self.row_weights_flag = True
#        print self.row_weights_flag

    def get_row_weights(self):
#        print self.row_weights_flag
        if not self.row_weights_flag:
#            print "  computing row weights"
            self.compute_row_weights()
#        print "  returning weights"
        return self.row_weights

    def get_basis_change(self):
        if not self.basis_change_flag:
            self.compute_basis_change()
        return self.basis_change
            
    def get_kernel(self):
        """
        Return Z2 vector space object. Basis elements are given as row
        vectors.
        """
        leading_term_list = [row.index(1) for row in 
                             self.get_rref().get_matrix() if 1 in row]
        free_variables = [index for index in 
                          range(0, self.get_rref().get_size()[1])
                          if index not in leading_term_list]
        kernel = ModTwoVectorSpace([])
        for column_index in free_variables:
            basis_element = {}
            for index in range(0,self.get_rref().get_size()[1]):
                basis_element[index] = 0
            for row in self.get_rref().get_matrix():
                if 1 in row:
                    leading_term = row.index(1)
                    if row[column_index] == 1:
                        basis_element[leading_term] = 1
            basis_element[column_index] = 1
            basis_vector = [basis_element[i] for i in 
                            range(0, self.get_rref().get_size()[1])]
            kernel.add_basis_element([basis_vector])
        return kernel

    def can_solve(self, vector):
        """
        
        """
        if type(vector) == list:
            append_vector = ModTwoMatrix([vector])
            append_vector.transpose()
        elif isinstance(vector, ModTwoMatrix):
            if vector.get_size() != (self.get_size()[0], 1):
                raise TypeError
            append_vector = vector
        else:
            raise TypeError("vector not of correct type / format")
#why is git not accepting this commit        
#        print "  Getting row weights"
        row_weights = self.get_row_weights()
#        print "  Getting vecotr in rref basis"
        append_vector = self.get_basis_change() * append_vector
        for index in range(0, self.get_size()[0]):
#            print "  checking at index" + str(index)
            if row_weights[index]:
                pass
            else:
                if append_vector.get_matrix()[index][0]:
                    return False
        return True

    # def slow_can_solve(self, vector):
    #     """
    #     Returns true if can solve Ax = b, where A is self, b is
    #     vector.  Returns error if size is incorrect.  Row vector form
    #     for input vector, or matrix representing a row or column
    #     vector.
    #     """
    #     new_matrix = self.copy().get_matrix()
    #     append_vector = vector
    #     if len(append_vector) != self.get_size()[0]:
    #         raise ValueError
    #     for row_index in range(0,len(new_matrix)):
    #         new_matrix[row_index].append(append_vector[row_index])
    #     augmented_matrix = ModTwoMatrix(new_matrix)
    #     augmented_matrix.row_reduce()
    #     for row in augmented_matrix.get_matrix():
    #         if (1 in row and row.index(1) == 
    #             augmented_matrix.get_size()[1] - 1):
    #             return False
    #         else:
    #             pass
    #     return True

def matrix_from_array(array, size):
    new_matrix = []
    for i in range(0, size[0]):
        new_row = []
        for j in range(0, size[1]):
            new_row.append(array[(i,j)])
        new_matrix.append(new_row)
    return ModTwoMatrix(new_matrix)

def identity_matrix(size):
    if size[0] != size[1]:
        raise ValueError
    key_list = [(i, j) for i in range(0, size[0]) for j in range(0, size[1])]
    array = {}
    for key in key_list:
        array[key] = 0
    for index in range(0, min(size[0], size[1])):
        array[(index, index)] = 1
    return matrix_from_array(array, size)

def elementary_column_vector(size, entry):
    """
    size is just an integer indicating number of rows.
    Indexing starts at 0, so 0 <= entry < size
    """
    new_matrix = []
    for i in range(0, size):
        if i == entry:
            new_matrix.append(1)
        else:
            new_matrix.append(0)
    result = Mod2Matrix(new_matrix)
    result.transpose()
    return result

def zero_matrix(size):
    key_list = [(i, j) for i in range(0, size[0]) for j in range(0, size[1])]
    array = {}
    for key in key_list:
        array[key] = 0
    return matrix_from_array(array, size)

def row_operation_matrix(i, j, size):        
    """
    adds row i to row j
    """
    if size[0] != size[1]:
        raise ValueError
    if i == j:
        raise ValueError
    key_list = [(x, y) for x in range(0, size[0]) for y in range(0, size[1])]
    array = {}
    for key in key_list:
        array[key] = 0
    for index in range(0, min(size[0], size[1])):
        array[(index, index)] = 1
    array[(j, i)] = 1
    return matrix_from_array(array, size)
        
def random_matrix(size):
    new_matrix = []
    for i in range(0,size[0]):
        new_row = []
        for j in range(0,size[1]):
            new_row.append(random.choice((0,1)))
        new_matrix.append(new_row)
    return ModTwoMatrix(new_matrix)

            
