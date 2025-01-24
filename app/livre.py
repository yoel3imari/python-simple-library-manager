from app.database import Database


class Livre:

    def __init__(self, titre="", auteur="", annee_pub="", database: Database = None):
        self.titre = titre
        self.auteur = auteur
        self.annee_pub = annee_pub
        self.db = database

        if self.db:
            self.table_name = "livres"
            self.db.create_table(
                self.table_name,
                {
                    "titre": "TEXT NOT NULL UNIQUE",
                    "auteur": "TEXT NOT NULL",
                    "annee_pub": "TEXT NOT NULL",
                    'user_id': "INTEGER NOT NULL"
                },
            )

    def create(self, data):
        """
        Inserts a new Livre record into the database.
        """
        self.db.insert(self.table_name, data)

    def get_all_books(self):
        """
        Fetches all Livre records from the database.
        """
        rows = self.db.fetch_all(self.table_name)
        return [Livre.from_row(row) for row in rows]

    def get_one(self, livre_title):
        """
        Fetches a single Livre record by its ID.
        """
        row = self.db.fetch_one(self.table_name, "titre = ?", (livre_title,))
        return Livre.from_row(row)

    def update(self, livre_title, data):
        """
        Updates an existing Livre record in the database.
        """
        self.db.update(self.table_name, data, "titre = ?", (livre_title,))

    def delete(self, livre_title):
        """
        Deletes a Livre record from the database.
        """
        self.db.delete(self.table_name, "titre = ?", (livre_title,))

    def __str__(self):
        return f"- {self.titre} [{self.auteur}]({self.annee_pub})"

    def to_row(self):
        """convertit le livre en list

        Returns:
            _type_: List[Livre]
        """
        return {"titre": self.titre, "auteur": self.auteur, "annee_pub": self.annee_pub}

    @classmethod
    def from_row(cls, row):
        """
        Converts a database row (tuple) into a Livre instance.
        """
        if not row:
            return None
        return cls(titre=row[1], auteur=row[2], annee_pub=row[3])
