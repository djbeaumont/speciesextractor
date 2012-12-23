import unittest
from .. import parse

class TestParse(unittest.TestCase):
	"""
	Run with: python -m speciesextractor.test discover --pattern=*.py
	"""

	def test_should_find_binomial_name(self):
		result = parse.is_binomial_form('Turdus merula')
		self.assertTrue(result)

	def test_should_not_find_lower_case_binomial_name(self):
		result = parse.is_binomial_form('turdus merula')
		self.assertFalse(result)

	def test_should_not_find_single_word_binomial_name(self):
		result = parse.is_binomial_form('Turdus')
		self.assertFalse(result)

if __name__ == '__main__':
	unittest.main()
