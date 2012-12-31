import argparse
from .downloader import Downloader
from .parser import Parser
from .inserter import Inserter

def main():
    """Entry point into the application. Parse options and arguments."""

    argparser = argparse.ArgumentParser(description='Download, extract and import species data.')
    argparser.add_argument('location', metavar='L', type=str, help='location of the wikispecies dump')

    args = argparser.parse_args()

    filelocation = None
    if args.location.startswith('http'):
        downloader = Downloader()
        filelocation = downloader.download(args.location)
    else:
        filelocation = args.location

    parser = Parser(args.location)
    parser.parse()

    sorted_species = sorted(parser.all_species, key=lambda s: s.binomial_name)

    inserter = Inserter()

    inserter.insert_locales(parser.locales)
    inserter.insert(sorted_species)
