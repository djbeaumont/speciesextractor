import psycopg2 as dbapi2

class Inserter:
    """Insert species records into a database"""

    def __init__(self):
        """Construct an Inserter"""
        self.db = dbapi2.connect(database="censeo", user="censeo", password="censeo")
	
    def insert(self, all_species):
        """Perform database inserts"""
        cur = self.db.cursor()
        species_insert_tpl = "INSERT INTO species (id) VALUES ('%s')"
        name_insert_tpl = ""

        for species in all_species:
            species_id = species.binomial_name.upper().replace(' ', '_')
            try:
                cur.execute(species_insert_tpl % species_id)
                for locale in species.vernacular_names.keys():
                    # save vernacular names
                    # TODO
                    pass
                self.db.commit()
            except:
                self.db.rollback()
                print("Could not save species: %s" % species_id)

    def insert_locales(self, locales):
        """Save locales of vernacular names"""
        cur = self.db.cursor()
        locale_insert_tpl = "INSERT INTO locales (id) VALUES ('%s')"

        for locale in locales:
            try:
                cur.execute(locale_insert_tpl % locale)
                self.db.commit()
            except:
                self.db.rollback()
                print("Could not save locale: %s" % locale)
