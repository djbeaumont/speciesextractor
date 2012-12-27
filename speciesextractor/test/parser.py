import unittest
from ..parser import Parser

class TestParser(unittest.TestCase):
    """
    Run with: python3 -m unittest discover --pattern=*.py
    """

    def setUp(self):
        self.parser = Parser('')

    def test_should_find_binomial_name(self):
        result = self.parser.is_binomial_form('Turdus merula')
        self.assertTrue(result)

    def test_should_not_find_lower_case_binomial_name(self):
        result = self.parser.is_binomial_form('turdus merula')
        self.assertFalse(result)

    def test_should_not_find_single_word_binomial_name(self):
        result = self.parser.is_binomial_form('Turdus')
        self.assertFalse(result)

    def test_should_not_find_triple_word_binomial_name(self):
        result = self.parser.is_binomial_form('Turdus merula merula')
        self.assertFalse(result)

    def test_should_find_taxonavigation_section(self):
        result = self.parser.has_taxonavigation('filler\n== Taxonavigation ==more filler')
        self.assertTrue(result)

    def test_should_find_taxonavigation_section_without_spaces(self):
        result = self.parser.has_taxonavigation('filler\n==Taxonavigation==\nmore filler')
        self.assertTrue(result) 

    def test_should_not_find_taxonavigation_section(self):
        result = self.parser.has_taxonavigation('filler\n==Tax==\nmore filler')
        self.assertFalse(result)

    def test_should_split_sections(self):
        page_text = "== Reference==\nContent\n==Vernacular names==\nMore content"
        sections = self.parser.split_wiki_sections(page_text)
        self.assertEqual(["", "== Reference==", "\nContent\n", "==Vernacular names==", "\nMore content"], sections)

    def test_should_find_vernacular_names(self):
        page_text = "== Reference ==\n* {{LSN10|170}}\n\n== Vernacular names ==\n{{VN\n|en=Blackbird, Ouzel\n|fr=Merle, Merle noir\n}}"
        names = self.parser.parse_vernacular_names(page_text)
        self.assertEqual({'en': ['Blackbird', 'Ouzel'], 'fr': ['Merle', 'Merle noir']}, names)
