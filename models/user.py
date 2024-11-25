import uuid

class User:
    def __init__(self, name, library_id=None, user_id=None):
        self.id = user_id
        self.name = name
        self.library_id = library_id or self._generate_library_id()

    @staticmethod
    def _generate_library_id():
        """Generate a unique library ID"""
        return f"LIB-{str(uuid.uuid4())[:8]}"

    @staticmethod
    def add_user(db, name):
        """Add a new user to the database"""
        library_id = f"LIB-{str(uuid.uuid4())[:8]}"
        query = """
        INSERT INTO users (name, library_id)
        VALUES (%s, %s)
        """
        params = (name, library_id)
        return db.execute_query(query, params)

    @staticmethod
    def get_all_users(db):
        """Retrieve all users from the database"""
        query = "SELECT * FROM users"
        return db.execute_query(query)

    @staticmethod
    def get_user_by_id(db, user_id):
        """Retrieve user details by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = db.execute_query(query, (user_id,))
        return result[0] if result else None

    @staticmethod
    def get_user_by_library_id(db, library_id):
        """Retrieve user details by library ID"""
        query = "SELECT * FROM users WHERE library_id = %s"
        result = db.execute_query(query, (library_id,))
        return result[0] if result else None

    @staticmethod
    def get_borrowed_books(db, user_id):
        """Get all books currently borrowed by the user"""
        query = """
        SELECT b.*, bb.borrow_date, bb.return_date
        FROM books b
        JOIN borrowed_books bb ON b.id = bb.book_id
        WHERE bb.user_id = %s AND bb.return_date IS NULL
        """
        return db.execute_query(query, (user_id,))

    @staticmethod
    def get_borrowing_history(db, user_id):
        """Get user's complete borrowing history"""
        query = """
        SELECT b.*, bb.borrow_date, bb.return_date
        FROM books b
        JOIN borrowed_books bb ON b.id = bb.book_id
        WHERE bb.user_id = %s
        ORDER BY bb.borrow_date DESC
        """
        return db.execute_query(query, (user_id,))
