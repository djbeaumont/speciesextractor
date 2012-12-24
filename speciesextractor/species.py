class Species:
    """Representation of a species"""

    def __init__(self, binomial_name, vernacular_names):
        """Construct a species from its binomial name and vernacular_names"""
        self.binomial_name = binomial_name
        self.vernacular_names = vernacular_names

    def __str__(self):
        """String representation of this Species"""
        return 'Species: %s' % self.binomial_name

    def __repr__(self):
        """String representation of this Species for a REPL"""
        return '<%s>' % self.__str__()
