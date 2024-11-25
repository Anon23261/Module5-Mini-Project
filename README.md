# 📚 Library Management System

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-v8.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A modern, feature-rich Library Management System that seamlessly integrates Python with MySQL database. This system provides a comprehensive solution for managing books, users, and authors in a library setting.

## ✨ Features

### 📖 Book Management
- Add and catalog new books with detailed information
- Track book availability in real-time
- Efficient book search by title or ISBN
- Comprehensive borrowing and return system

### 👥 User Management
- Secure user registration system
- Automatic generation of unique library IDs
- Track user borrowing history
- User profile management

### ✍️ Author Management
- Detailed author profiles with biographies
- Track author's published works
- Easy author lookup and book association

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/Anon23261/Module5-Mini-Project.git
cd Module5-Mini-Project
```

2. Set up a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Database Setup
```sql
-- Create database
CREATE DATABASE library_db;
USE library_db;

-- Create tables
CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT,
    isbn VARCHAR(13) NOT NULL,
    publication_date DATE,
    availability BOOLEAN DEFAULT 1,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    library_id VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE borrowed_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    borrow_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
```

5. Configure Database Connection
- Navigate to `database/connection.py`
- Update MySQL credentials:
```python
host='localhost'
user='your_username'
password='your_password'
database='library_db'
```

### 🎮 Running the Application

```bash
python main.py
```

## 🏗️ Project Structure

```
Library-Management-System/
├── database/
│   ├── connection.py     # Database connection handler
│   └── queries.py        # SQL query manager
├── models/
│   ├── book.py          # Book class and operations
│   ├── user.py          # User class and operations
│   └── author.py        # Author class and operations
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── LICENSE             # MIT license
└── README.md           # Project documentation
```

## 💡 Usage Examples

### Adding a New Book
```python
# Through CLI menu:
1. Select "Book Operations"
2. Choose "Add a new book"
3. Enter book details when prompted
```

### Registering a User
```python
# Through CLI menu:
1. Select "User Operations"
2. Choose "Add a new user"
3. Enter user details
```

### Managing Authors
```python
# Through CLI menu:
1. Select "Author Operations"
2. Choose desired operation
3. Follow the prompts
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Inspired by modern library management systems
- Built with Python and MySQL

## 📞 Contact

Anon23261 - [GitHub Profile](https://github.com/Anon23261)

Project Link: [https://github.com/Anon23261/Module5-Mini-Project](https://github.com/Anon23261/Module5-Mini-Project)
