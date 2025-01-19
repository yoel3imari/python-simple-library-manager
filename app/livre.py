class Livre:
    
    def __init__(self, titre="", auteur="", annee_pub=""):
        self.titre = titre
        self.auteur = auteur
        self.annee_pub = annee_pub
    
    def __str__(self):
        return f'- {self.titre} [{self.auteur}]({self.annee_pub})'
    
    def toRow(self):
        """convertit le livre en list

        Returns:
            _type_: List[Livre]
        """
        return {
            "titre": self.titre,
            "auteur": self.auteur,
            "annee_pub": self.annee_pub
        }