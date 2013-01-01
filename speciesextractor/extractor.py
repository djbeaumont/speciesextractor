import argparse
from .downloader import Downloader
from .parser import Parser
from .inserter import Inserter

def main():
    """Entry point into the application. Parse options and arguments."""

    argparser = argparse.ArgumentParser(description='Download, extract and import species data.')
    argparser.add_argument('location',
                            metavar='L',
                            type=str,
                            help='location of the wikispecies dump')

    databases = argparser.add_mutually_exclusive_group(required=True)
    databases.add_argument('--sqlite', action='store_true', help='save species to a SQLite database')
    databases.add_argument('--postgresql', action='store_true', help='save species to a PostgreSQL database')

    sqliteopts = argparser.add_argument_group(
        'SQLite Options', 'Configuration of saving species to a SQLite database')
    sqliteopts.add_argument('-o', '--output',
                            metavar='FILENAME',
                            type=str,
                            help='filename for new SQLite species database')

    postgresopts = argparser.add_argument_group(
        'PostgreSQL Options', 'Configuration of saving species to a PostgreSQL database')
    postgresopts.add_argument('-d', '--database', help='name of the database to insert species data into')
    postgresopts.add_argument('-u', '--username', help='username to connect to the database server')
    postgresopts.add_argument('-p', '--password', help='password to connect to the database server')

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
