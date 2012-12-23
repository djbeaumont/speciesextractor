from xml.etree import cElementTree as etree

ns = {
	'n': 'http://www.mediawiki.org/xml/export-0.8/'
}

def parse(local_location):
	"""
	Read XML out of a file and produce an object tree of species
	"""
	
	page_tag = '{%s}%s' % (ns['n'], 'page')
	for event, element in etree.iterparse(local_location):
		if element.tag == page_tag:
			parse_page(element)

		# Clear memory
		#element.clear()

def parse_page(page):
	"""
	Parse the contents of a page element
	"""

	page_title = page.findtext('n:title', namespaces=ns)
	page_text = page.findtext('n:text', namespaces=ns)

	print(page_title)
