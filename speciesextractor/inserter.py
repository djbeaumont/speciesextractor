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
                # TODO - insert vernacular names
                self.db.commit()
            except:
                self.db.rollback()
                print("Could not save species: %s" % species_id)
