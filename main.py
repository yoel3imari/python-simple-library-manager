import os
import platform
from colorama import Fore
from app.biblio import Biblio
from app.livre import Livre

def clear_terminal():
    """Clear the terminal screen."""
    # Check the operating system and run the appropriate command
    system_name = platform.system().lower()
    # Clear the terminal based on the OS
    if system_name == 'windows':
        os.system('cls')  # Windows
    else:
        os.system('clear')  # macOS, Linux, and other Unix-like systems

def afficher_menu():
    # clear_terminal()
    print(Fore.CYAN, "\n--- Gestion de la Bibliothèque ---")
    print(Fore.RESET)
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Lister tous les livres")
    print("4. Sauvegarder les livres dans un fichier")
    print("5. Charger les livres depuis un fichier")
    print("6. Quitter")

def main():
    biblio = Biblio()
    clear_terminal()
    try:
        while True:
            afficher_menu()
            choix = input("Choisissez une option (1-6): ")

            if choix == "1":
                # Ajouter un livre
                titre = input("- le titre du livre: ")
                auteur = input("- l'auteur du livre: ")
                annee_pub = input("- l'année de publication (AAAA): ")
                try:
                    livre = Livre(titre, auteur, annee_pub)
                    biblio.add_book(livre)
                    print(Fore.GREEN, "Livre ajouté avec succès !")
                except ValueError as e:
                    print(Fore.RED, f"Erreur: {e}")

            elif choix == "2":
                # Supprimer un livre
                titre = input("- le titre du livre à supprimer: ")
                try:
                    biblio.remove_book(titre)
                    print(Fore.GREEN, "Livre supprimé avec succès !")
                except ValueError as e:
                    print(Fore.RED, f"Erreur: {e}")

            elif choix == "3":
                # Lister tous les livres
                print("\nListe des livres :")
                biblio.show_books()

            elif choix == "4":
                # Sauvegarder les livres dans un fichier
                fichier = input("- le nom du fichier pour sauvegarder: ")
                try:
                    biblio.save_books(file_name=fichier)
                    print(Fore.GREEN, f"Livres sauvegardés dans {fichier or 'books.csv'} avec succès !")
                    print(Fore.RESET)
                except Exception as e:
                    print(Fore.RED, f"Erreur lors de la sauvegarde: {e}")

            elif choix == "5":
                # Charger les livres depuis un fichier
                fichier = input("- le nom du fichier pour charger: ")
                try:
                    biblio.load_books(fichier)
                    print(Fore.GREEN, f"Livres chargés depuis {fichier or 'books.csv'} avec succès !")
                except Exception as e:
                    print(Fore.RED, f"Erreur lors du chargement: {e}")

            elif choix == "6":
                # Quitter le programme
                print(Fore.CYAN, "Merci d'avoir utilisé le programme. Au revoir !")
                break

            else:
                print(Fore.RED, "Option invalide. Veuillez choisir une option entre 1 et 6.")
    except KeyboardInterrupt:
        print(Fore.YELLOW, "\nMerci d'avoir utilisé le programme. Au revoir !")
        exit(0)  # Exit the program with a status code of 0 (success)

    

if __name__ == "__main__":
    main()