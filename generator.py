class Generator(object):
    def __init__(self, name, degree):
        """Name is to be a string, and degree is a tuple of integers of the
        appropriate length for the given context.

        """
        self.name = name
        self.degree = degree

    def get_name(self):
        return self.name

    def get_degree(self, options):
        return self.degree

    def is_equal_to(self, generator):
        return (self.get_name() == generator.get_name() and 
                self.get_degree() == generator.get_degree() )
