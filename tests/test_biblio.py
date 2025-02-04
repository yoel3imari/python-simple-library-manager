import csv
import os
import unittest

from app.biblio import DATA_FOLDER, Biblio
from app.livre import Livre

class TestBiblio(unittest.TestCase):

    def setUp(self):
        self.biblio = Biblio()
        self.livre1 = Livre("aaa", "bbb", "1245")
        self.livre2 = Livre("ccc", "ddd", "1949")
        self.default_file = os.path.join(DATA_FOLDER, "books.csv")
        self.test_file = os.path.join(DATA_FOLDER, "test_books.csv")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        self.assertIn(self.livre1, self.biblio.book_list)
    
    def test_add_book_with_missing_fields(self):
        with self.assertRaises(ValueError):
            self.biblio.add_book(Livre("","xxx", "4578"))
        
        with self.assertRaises(ValueError):
            self.biblio.add_book(Livre("xxx", "", "4578"))

    def test_remove_book(self):
        self.biblio.add_book(self.livre1)
        self.biblio.remove_book(self.livre1.titre)
        self.assertNotIn(self.livre1, self.biblio.book_list)

    def test_remove_nonexistent_book(self):
        with self.assertRaises(ValueError):
            self.biblio.remove_book("Nonexistent Book")

    def test_show_books(self):
        self.biblio.add_book(self.livre1)
        self.biblio.add_book(self.livre2)
        self.biblio.show_books()

    def test_save_books(self):
        self.biblio.add_book(self.livre1)
        self.biblio.add_book(self.livre2)
        self.biblio.save_books()

        self.assertTrue(os.path.exists(self.default_file))
        with open(self.default_file, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0][0], "aaa")
            self.assertEqual(rows[1][0], "ccc")

    def test_save_books_to_new_file(self):
        self.biblio.add_book(self.livre1)
        self.biblio.add_book(self.livre2)
        
        self.biblio.save_books(self.test_file)

        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["titre"], "aaa")
            self.assertEqual(rows[1]["titre"], "ccc")

    def test_load_books(self):
        self.biblio.add_book(self.livre1)
        self.biblio.add_book(self.livre2)
        self.biblio.save_books(self.test_file)

        new_biblio = Biblio()
        new_biblio.load_books(self.test_file)

        self.assertEqual(len(new_biblio.book_list), 2)
        self.assertEqual(new_biblio.book_list[0].titre, "aaa")
        self.assertEqual(new_biblio.book_list[1].titre, "ccc")

    def test_load_books_from_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.biblio.load_books("nonexistent_file.csv")

    