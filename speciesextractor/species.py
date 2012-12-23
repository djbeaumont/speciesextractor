class Species:
	"""Representation of a species"""

	def __init__(self, binomial_name):
		"""Construct a species from its binomial name"""
		self.binomial_name = binomial_name

	def __str__(self):
		"""String representation of this Species"""
		return 'Species: %s' % self.binomial_name

	def __repr__(self):
		"""String representation of this Species for a REPL"""
		return '<%s>' % self.__str__()
