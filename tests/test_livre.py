import unittest

from app.livre import Livre


class TestLivre(unittest.TestCase):
    def test_livre_initialization(self):
        livre = Livre("aaa", "aaa", "1555")
        self.assertEqual(livre.titre, "aaa")
        self.assertEqual(livre.auteur, "aaa")
        self.assertEqual(livre.annee_pub, "1555")

    def test_livre_str(self):
        livre = Livre("aaa", "aaa", "4578")
        expected_str = '- "aaa [aaa](4578)"'
        self.assertEqual(str(livre), expected_str)

    def test_livre_to_row(self):
        livre = Livre("aaa", "aaa", "1943")
        expected_row = {
            "titre": "aaa",
            "auteur": "-aaa",
            "annee_pub": "1943",
        }
        self.assertEqual(livre.to_row(), expected_row)
