from xml.etree import cElementTree as etree
import re

class Parser:
	"""
	Parser to read XML files and represent data as python objects
	"""

	def __init__(self, local_location):
		"""
		Construct a parser with the XML file's local location
		"""
		self.local_location = local_location
		self.ns = {'n': 'http://www.mediawiki.org/xml/export-0.8/'}
		self.all_species = []

	def parse(self):
		"""
		Read XML out of a file and produce an object tree of species
		"""
		
		page_tag = '{%s}%s' % (self.ns['n'], 'page')
		for event, element in etree.iterparse(self.local_location):
			if element.tag == page_tag:
				self.parse_page(element)

			# Clear memory
			#element.clear()

	def parse_page(self, page):
		"""
		Parse the contents of a page element
		"""

		page_title = page.findtext('n:title', namespaces=self.ns)
		page_text = page.findtext('n:revision/n:text', namespaces=self.ns)

		# Split the page text based on wikitext headings
		sections = re.split('(==\s*\w+\s*==)', page_text)

		print(page_title)
		print(sections)

	def is_species_page(self, title, text):
		"""
		Does this page contain a species with a standardised binomial name
		"""
		# TODO
		return True

	def is_template_page(self, title, text):
		"""
		Is this page a template
		"""
		# TODO
		return False

	def is_binomial_form(self, title):
		"""
		Check if the page title matches the binomial naming format
		"""
		return re.match('^[A-Z]{1}[a-z]+ [a-z]+$', title) != None

	def has_taxonavigation(self, text):
		"""
		Check if the page text contains a 'Taxonavigation' section
		"""
		return re.search('==[\s]?Taxonavigation[\s]?==', text) != None