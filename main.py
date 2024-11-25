from database.connection import DatabaseConnection
from models.book import Book
from models.author import Author
from models.user import User
from datetime import datetime

class LibraryManagementSystem:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def display_main_menu(self):
        while True:
            print("\nLibrary Management System")
            print("=" * 25)
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.book_menu()
            elif choice == '2':
                self.user_menu()
            elif choice == '3':
                self.author_menu()
            elif choice == '4':
                print("\nThank you for using the Library Management System!")
                self.db.disconnect()
                break
            else:
                print("\nInvalid choice. Please try again.")

    def book_menu(self):
        while True:
            print("\nBook Operations")
            print("=" * 25)
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Search for a book")
            print("5. Display all books")
            print("6. Back to main menu")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.borrow_book()
            elif choice == '3':
                self.return_book()
            elif choice == '4':
                self.search_book()
            elif choice == '5':
                self.display_all_books()
            elif choice == '6':
                break
            else:
                print("\nInvalid choice. Please try again.")

    def user_menu(self):
        while True:
            print("\nUser Operations")
            print("=" * 25)
            print("1. Add a new user")
            print("2. View user details")
            print("3. Display all users")
            print("4. Back to main menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_user_details()
            elif choice == '3':
                self.display_all_users()
            elif choice == '4':
                break
            else:
                print("\nInvalid choice. Please try again.")

    def author_menu(self):
        while True:
            print("\nAuthor Operations")
            print("=" * 25)
            print("1. Add a new author")
            print("2. View author details")
            print("3. Display all authors")
            print("4. Back to main menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.add_author()
            elif choice == '2':
                self.view_author_details()
            elif choice == '3':
                self.display_all_authors()
            elif choice == '4':
                break
            else:
                print("\nInvalid choice. Please try again.")

    # Book Operations
    def add_book(self):
        print("\nAdd a New Book")
        print("=" * 25)
        title = input("Enter book title: ")
        isbn = input("Enter ISBN: ")
        
        # Display authors for selection
        authors = Author.get_all_authors(self.db)
        if not authors:
            print("No authors available. Please add an author first.")
            return
            
        print("\nAvailable Authors:")
        for author in authors:
            print(f"{author['id']}: {author['name']}")
            
        author_id = input("Enter author ID: ")
        pub_date = input("Enter publication date (YYYY-MM-DD): ")
        
        try:
            Book.add_book(self.db, title, int(author_id), isbn, pub_date)
            print("\nBook added successfully!")
        except Exception as e:
            print(f"\nError adding book: {str(e)}")

    def borrow_book(self):
        print("\nBorrow a Book")
        print("=" * 25)
        library_id = input("Enter user's library ID: ")
        user = User.get_user_by_library_id(self.db, library_id)
        
        if not user:
            print("User not found!")
            return
            
        # Display available books
        books = Book.get_all_books(self.db)
        print("\nAvailable Books:")
        for book in books:
            if book['availability']:
                print(f"{book['id']}: {book['title']} by {book['author_name']}")
                
        book_id = input("Enter book ID to borrow: ")
        success, message = Book.borrow_book(self.db, int(book_id), user['id'])
        print(message)

    def return_book(self):
        print("\nReturn a Book")
        print("=" * 25)
        library_id = input("Enter user's library ID: ")
        user = User.get_user_by_library_id(self.db, library_id)
        
        if not user:
            print("User not found!")
            return
            
        # Display borrowed books
        borrowed_books = User.get_borrowed_books(self.db, user['id'])
        if not borrowed_books:
            print("No books currently borrowed by this user.")
            return
            
        print("\nBorrowed Books:")
        for book in borrowed_books:
            print(f"{book['id']}: {book['title']}")
            
        book_id = input("Enter book ID to return: ")
        success, message = Book.return_book(self.db, int(book_id), user['id'])
        print(message)

    def search_book(self):
        print("\nSearch for a Book")
        print("=" * 25)
        search_term = input("Enter book title or ISBN to search: ")
        books = Book.search_book(self.db, search_term)
        
        if not books:
            print("No books found matching your search.")
            return
            
        print("\nSearch Results:")
        for book in books:
            status = "Available" if book['availability'] else "Borrowed"
            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author_name']}")
            print(f"ISBN: {book['isbn']}")
            print(f"Status: {status}")
            print("-" * 25)

    def display_all_books(self):
        print("\nAll Books")
        print("=" * 25)
        books = Book.get_all_books(self.db)
        
        if not books:
            print("No books in the library.")
            return
            
        for book in books:
            status = "Available" if book['availability'] else "Borrowed"
            print(f"ID: {book['id']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author_name']}")
            print(f"ISBN: {book['isbn']}")
            print(f"Status: {status}")
            print("-" * 25)

    # User Operations
    def add_user(self):
        print("\nAdd a New User")
        print("=" * 25)
        name = input("Enter user's name: ")
        user_id = User.add_user(self.db, name)
        print(f"\nUser added successfully! Library ID: {user_id}")

    def view_user_details(self):
        print("\nView User Details")
        print("=" * 25)
        library_id = input("Enter user's library ID: ")
        user = User.get_user_by_library_id(self.db, library_id)
        
        if not user:
            print("User not found!")
            return
            
        print(f"\nUser Details:")
        print(f"Name: {user['name']}")
        print(f"Library ID: {user['library_id']}")
        
        # Display borrowed books
        borrowed_books = User.get_borrowed_books(self.db, user['id'])
        if borrowed_books:
            print("\nCurrently Borrowed Books:")
            for book in borrowed_books:
                print(f"- {book['title']} (Borrowed on: {book['borrow_date']})")

    def display_all_users(self):
        print("\nAll Users")
        print("=" * 25)
        users = User.get_all_users(self.db)
        
        if not users:
            print("No users registered.")
            return
            
        for user in users:
            print(f"Name: {user['name']}")
            print(f"Library ID: {user['library_id']}")
            print("-" * 25)

    # Author Operations
    def add_author(self):
        print("\nAdd a New Author")
        print("=" * 25)
        name = input("Enter author's name: ")
        biography = input("Enter author's biography (optional): ")
        Author.add_author(self.db, name, biography if biography else None)
        print("\nAuthor added successfully!")

    def view_author_details(self):
        print("\nView Author Details")
        print("=" * 25)
        authors = Author.get_all_authors(self.db)
        
        if not authors:
            print("No authors available.")
            return
            
        print("\nAvailable Authors:")
        for author in authors:
            print(f"{author['id']}: {author['name']}")
            
        author_id = input("\nEnter author ID: ")
        author = Author.get_author_by_id(self.db, int(author_id))
        
        if not author:
            print("Author not found!")
            return
            
        print(f"\nAuthor Details:")
        print(f"Name: {author['name']}")
        if author['biography']:
            print(f"Biography: {author['biography']}")
            
        # Display author's books
        books = Author.get_author_books(self.db, author['id'])
        if books:
            print("\nBooks by this author:")
            for book in books:
                status = "Available" if book['availability'] else "Borrowed"
                print(f"- {book['title']} ({status})")

    def display_all_authors(self):
        print("\nAll Authors")
        print("=" * 25)
        authors = Author.get_all_authors(self.db)
        
        if not authors:
            print("No authors available.")
            return
            
        for author in authors:
            print(f"ID: {author['id']}")
            print(f"Name: {author['name']}")
            if author['biography']:
                print(f"Biography: {author['biography']}")
            print("-" * 25)

if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    library_system.display_main_menu()
