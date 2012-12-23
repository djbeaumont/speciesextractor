from xml.etree import cElementTree as etree
from .species import Species
import re

class Parser:
	"""Parser to read XML files and represent data as python objects"""

	def __init__(self, local_location):
		"""Construct a parser with the XML file's local location"""

		self.local_location = local_location
		self.ns = {'n': 'http://www.mediawiki.org/xml/export-0.8/'}
		self.all_species = []

	def parse(self):
		"""Read XML out of a file and produce an object tree of species"""
		
		page_tag = '{%s}%s' % (self.ns['n'], 'page')
		for event, element in etree.iterparse(self.local_location):
			if element.tag == page_tag:
				page_title = element.findtext('n:title', namespaces=self.ns)
				page_text = element.findtext('n:revision/n:text', namespaces=self.ns)

				if self.is_species_page(page_title, page_text):
					s = Species(page_title)
					self.all_species.append(s)

				# Split the page text based on wikitext headings
				#sections = re.split('(==\s*\w+\s*==)', page_text)

				# Clear memory
				element.clear()

	def is_species_page(self, title, text):
		"""Does this page contain a species with a standardised binomial name"""

		return self.is_binomial_form(title) and self.has_taxonavigation(text)

	def is_template_page(self, title, text):
		"""Is this page a template"""

		# TODO
		return False

	def is_binomial_form(self, title):
		"""Check if the page title matches the binomial naming format"""
		return re.match('^[A-Z]{1}[a-z]+ [a-z]+$', title) != None

	def has_taxonavigation(self, text):
		"""Check if the page text contains a 'Taxonavigation' section"""
		
		return re.search('==[\s]?Taxonavigation[\s]?==', text) != None
