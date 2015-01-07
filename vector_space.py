class ModTwoVectorSpace(object):
    def __init__(self, basis_list):
        self.basis_list = basis_list

    def __str__(self):
        output = "<"
        for basis_element in self.get_basis():
            output = output + str(basis_element) + ","
        output = output + ">"
        return output

    def __getstate__(self):
        return {'basis_list' : self.get_basis() }

    def __setstate__(self, _dict):
        self.basis_list = _dict['basis_list']
        
    def get_basis(self):
        return self.basis_list

    def add_basis_element(self, a_list):
        self.basis_list = self.basis_list + a_list
