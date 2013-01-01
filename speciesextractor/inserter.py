import uuid

class Inserter:
    """Insert species records into a database."""

    def __init__(self, connection, paramstyle):
        """Construct an Inserter"""
        self.db = connection

        species_insert_tpl = "INSERT INTO species (id) VALUES ($$)"
        name_insert_tpl = "INSERT INTO vernacular_names (id, name, species_id, locale_id) VALUES ($$, $$, $$, $$)"
        locale_insert_tpl = "INSERT INTO locales (id) VALUES ($$)"

        binding = '?' if paramstyle == 'qmark' else '%s'

        self.species_insert_tpl = species_insert_tpl.replace('$$', binding)
        self.name_insert_tpl = name_insert_tpl.replace('$$', binding)
        self.locale_insert_tpl = locale_insert_tpl.replace('$$', binding)
	
    def insert(self, all_species):
        """Perform database inserts"""
        cur = self.db.cursor()

        for species in all_species:
            species_id = species.binomial_name.upper().replace(' ', '_')
            try:
                cur.execute(self.species_insert_tpl, (species_id,))
                for locale in species.vernacular_names.keys():
                    # save vernacular names
                    for name in species.vernacular_names[locale]:
                        name_id = uuid.uuid4().hex
                        cur.execute(self.name_insert_tpl, (name_id, name, species_id, locale))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                print("Could not save species: %s" % species_id)

    def insert_locales(self, locales):
        """Save locales of vernacular names"""
        cur = self.db.cursor()

        for locale in locales:
            try:
                cur.execute(self.locale_insert_tpl, (locale,))
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
                print("Could not save locale: %s" % locale)
