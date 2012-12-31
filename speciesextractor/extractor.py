from .parser import Parser
from .inserter import Inserter

def main():
    """Entry point into the application. Parse options and arguments."""
    
    parser = Parser('/Users/djb/Desktop/specieswiki-20121213-pages-meta-current.xml')
    parser.parse()

    sorted_species = sorted(parser.all_species, key=lambda s: s.binomial_name)

    inserter = Inserter()

    inserter.insert_locales(parser.locales)
    inserter.insert(sorted_species)
