class Author:
    def __init__(self, name, biography=None, author_id=None):
        self.id = author_id
        self.name = name
        self.biography = biography

    @staticmethod
    def add_author(db, name, biography=None):
        """Add a new author to the database"""
        query = """
        INSERT INTO authors (name, biography)
        VALUES (%s, %s)
        """
        params = (name, biography)
        return db.execute_query(query, params)

    @staticmethod
    def get_all_authors(db):
        """Retrieve all authors from the database"""
        query = "SELECT * FROM authors"
        return db.execute_query(query)

    @staticmethod
    def get_author_by_id(db, author_id):
        """Retrieve author details by ID"""
        query = "SELECT * FROM authors WHERE id = %s"
        result = db.execute_query(query, (author_id,))
        return result[0] if result else None

    @staticmethod
    def get_author_books(db, author_id):
        """Get all books by an author"""
        query = """
        SELECT b.* 
        FROM books b
        WHERE b.author_id = %s
        """
        return db.execute_query(query, (author_id,))

    @staticmethod
    def update_author(db, author_id, name=None, biography=None):
        """Update author information"""
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if biography:
            updates.append("biography = %s")
            params.append(biography)
            
        if not updates:
            return False, "No updates provided"
            
        query = f"""
        UPDATE authors 
        SET {', '.join(updates)}
        WHERE id = %s
        """
        params.append(author_id)
        
        db.execute_query(query, tuple(params))
        return True, "Author updated successfully"
