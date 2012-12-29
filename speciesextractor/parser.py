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
        self.locales = set()

    def parse(self):
        """Read XML out of a file and produce an object tree of species"""
        
        page_tag = '{%s}%s' % (self.ns['n'], 'page')
        for event, element in etree.iterparse(self.local_location):
            if element.tag == page_tag:
                page_title = element.findtext('n:title', namespaces=self.ns).strip()
                page_text = element.findtext('n:revision/n:text', namespaces=self.ns)

                if self.is_species_page(page_title, page_text):
                    names = self.parse_vernacular_names(page_text)
                    s = Species(page_title, names)
                    self.all_species.append(s)

                # Clear memory
                element.clear()

    def parse_vernacular_names(self, text):
        """Parse vernacular names from the page's wikitext"""
        vernacular_names_section = self.get_vernacular_names_section(text)

        parsed_vernacular_names = {}

        if vernacular_names_section != None:
            # parse section into a dictionary
            locale_names = re.findall('\|([a-z]{2,3})=([^\}|\|]+)', vernacular_names_section)
            for locale in locale_names:
                # Split out muliple names for the same locale
                self.locales.add(locale[0])
                parsed_vernacular_names[locale[0]] = [name.strip() for name in re.split(',', locale[1])]
        
        return parsed_vernacular_names

    def get_vernacular_names_section(self, text):
        """Get the wikitext matching the vernacular names section"""
        sections = self.split_wiki_sections(text)
        vernacular_names_section = None

        # Find the correct section of wikitext
        for section in sections:
            if re.match('^==[\s]?Vernacular names[\s]?==$', section) != None:
                vernacular_names_section = sections[sections.index(section) + 1]

        if vernacular_names_section != None:
            # Remove line breaks
            vernacular_names_section = vernacular_names_section.replace('\n', '')

            # Parse the names syntax block from the section
            match = re.search('\{\{VN[^\}]+\}\}', vernacular_names_section)

            return match.group(0) if match != None else None
        else:
            return None

    def split_wiki_sections(self, text):
        """Split wikitext into sections using headings"""
        return re.split('(^==.+)', text, flags=re.MULTILINE)

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
