from datetime import datetime
from database.connection import DatabaseConnection

class Book:
    def __init__(self, title, author_id, isbn, publication_date, book_id=None, availability=True):
        self.id = book_id
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publication_date = publication_date
        self.availability = availability

    @staticmethod
    def add_book(db, title, author_id, isbn, publication_date):
        """Add a new book to the database"""
        query = """
        INSERT INTO books (title, author_id, isbn, publication_date, availability)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (title, author_id, isbn, publication_date, True)
        return db.execute_query(query, params)

    @staticmethod
    def get_all_books(db):
        """Retrieve all books from the database"""
        query = """
        SELECT b.*, a.name as author_name 
        FROM books b 
        JOIN authors a ON b.author_id = a.id
        """
        return db.execute_query(query)

    @staticmethod
    def search_book(db, search_term):
        """Search for books by title or ISBN"""
        query = """
        SELECT b.*, a.name as author_name 
        FROM books b 
        JOIN authors a ON b.author_id = a.id
        WHERE b.title LIKE %s OR b.isbn LIKE %s
        """
        params = (f"%{search_term}%", f"%{search_term}%")
        return db.execute_query(query, params)

    @staticmethod
    def borrow_book(db, book_id, user_id):
        """Mark a book as borrowed and record the transaction"""
        # Check if book is available
        check_query = "SELECT availability FROM books WHERE id = %s"
        result = db.execute_query(check_query, (book_id,))
        
        if not result or not result[0]['availability']:
            return False, "Book is not available for borrowing"

        # Start transaction
        try:
            # Update book availability
            update_query = "UPDATE books SET availability = FALSE WHERE id = %s"
            db.execute_query(update_query, (book_id,))

            # Record borrowing
            borrow_query = """
            INSERT INTO borrowed_books (user_id, book_id, borrow_date)
            VALUES (%s, %s, %s)
            """
            db.execute_query(borrow_query, (user_id, book_id, datetime.now().date()))
            
            return True, "Book borrowed successfully"
        except Exception as e:
            return False, f"Error borrowing book: {str(e)}"

    @staticmethod
    def return_book(db, book_id, user_id):
        """Process a book return"""
        try:
            # Update book availability
            update_query = "UPDATE books SET availability = TRUE WHERE id = %s"
            db.execute_query(update_query, (book_id,))

            # Update borrowed_books record
            return_query = """
            UPDATE borrowed_books 
            SET return_date = %s
            WHERE book_id = %s AND user_id = %s AND return_date IS NULL
            """
            db.execute_query(return_query, (datetime.now().date(), book_id, user_id))
            
            return True, "Book returned successfully"
        except Exception as e:
            return False, f"Error returning book: {str(e)}"
