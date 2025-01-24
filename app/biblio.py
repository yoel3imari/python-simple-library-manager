import csv
import os
from typing import List

from app.livre import Livre

current_dir = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(current_dir, "..", "data")

class Biblio:
    def __init__(self, book_list: List[Livre]=[], file_name="books.csv"):
        self.book_list: List[Livre] = []

        self.load_books(file_name=file_name)
        for b in book_list:
            self.add_book(b)


    def add_book(self, book: Livre):
        """Ajouter un livre au biblio

        Args:
            book (Livre): Livre ()

        Raises:
            ValueError: si titre ou auteur est vide
        """
        if not book.titre or not book.auteur:
            raise ValueError('Le livre doit avoir un titre et un auteur')
        if not self.book_exists(book.titre, book.auteur):
            self.book_list.append(book)
    
    def book_exists(self, title: str, auteur: str) -> bool:
        livre = next((livre for livre in self.book_list if livre.titre == title), None)
        if not livre:
            return False
        return True
        
    
    def remove_book(self, title: str):
        """retirer un livre avec le titre

        Args:
            title (str): titre du livre à retirer

        Raises:
            ValueError: si livre n'existe pas
        """
        livre = next((livre for livre in self.book_list if livre.titre == title), None)
        if livre:
            self.book_list.remove(livre)
        else:
            raise ValueError(f'Le livre "{title}" n\'existe pas')
    
    def show_books(self):
        """
        Afficher les livres
        """
        if len(self.book_list) == 0:
            print("Pas de livres")
            return
        
        for livre in self.book_list :
            print(livre)

    def save_books(self, file_name: str="books.csv"):
        """sauvegarder les livres dans un ficher csv

        Args:
            file (str, optional): Nom du ficher. par default c'est books. si n'existe pas, il va être créé
        """
        default = "books.csv"
        if not file_name:
            file_name = default
        file_path = os.path.join(DATA_FOLDER, file_name)
        fieldnames = ["titre", "auteur", "annee_pub"]

        with open(file_path, "w") as books:
            writer = csv.DictWriter(books, fieldnames=fieldnames)
            for livre in self.book_list:
                writer.writerow(livre.to_row())
    
    def load_books(self, file_name: str="books.csv"):
        """Télécharger les livres sauvegarder dans un fichier csv

        Args:
            file (str, optional): Nom du fichier

        Raises:
            FileNotFoundError: si fichier n'existe pas

        Returns:
            _type_: list des livres
        """
        default = "books.csv"
        if not file_name:
            file_name = default
        file_path = os.path.join(DATA_FOLDER, file_name)
        # create file if not exist
        if not os.path.exists(file_path):
            open(file_path, "w").close()
    
        book_list = []
        with open(file_path, "r") as books:
            reader = csv.reader(books)
            for row in reader:
                book_list.append(Livre(row[0], row[1], row[2]))
        
        for b in book_list:
            self.add_book(b)

        return book_list
    
