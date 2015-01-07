class Generator(object):
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree

    def get_name(self):
        return self.name

    def get_degree(self, options):
        return self.degree

    def is_equal_to(self, generator):
        return (self.get_name() == generator.get_name() and 
                self.get_degree() == generator.get_degree() )
