import unittest
from .. import parse

class TestParse(unittest.TestCase):
	"""
	Run with: python -m speciesextractor.test.parse discover --pattern=*.py
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

	def test_should_not_find_triple_word_binomial_name(self):
		result = parse.is_binomial_form('Turdus merula merula')
		self.assertFalse(result)

	def test_should_find_taxonavigation_section(self):
		result = parse.has_taxonavigation('filler\n== Taxonavigation ==more filler')
		self.assertTrue(result)

	def test_should_find_taxonavigation_section_without_spaces(self):
		result = parse.has_taxonavigation('filler\n==Taxonavigation==\nmore filler')
		self.assertTrue(result)	

	def test_should_not_find_taxonavigation_section(self):
		result = parse.has_taxonavigation('filler\n==Tax==\nmore filler')
		self.assertTrue(result)

if __name__ == '__main__':
	unittest.main()
