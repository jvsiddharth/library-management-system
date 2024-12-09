# Library Management System API

A Flask-based REST API for managing a library system with support for books and members management.

## Features

- CRUD operations for books and members
- Search functionality for books by title or author
- Pagination support
- Token-based authentication
- Type-safe implementation
- Comprehensive test coverage

## Project Structure

```
library_management_system/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── member.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── books.py
│   │   └── members.py
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_members.py
├── venv/
├── README.md
├── requirements.txt
└── run.py
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python run.py
   ```

## API Documentation

### Authentication
- POST /auth/register - Register a new member
- POST /auth/login - Login and get access token

### Books
- GET /books - List all books (with pagination)
- GET /books/<id> - Get a specific book
- POST /books - Add a new book
- PUT /books/<id> - Update a book
- DELETE /books/<id> - Delete a book
- GET /books/search - Search books by title or author

### Members
- GET /members - List all members (with pagination)
- GET /members/<id> - Get a specific member
- POST /members - Add a new member
- PUT /members/<id> - Update a member
- DELETE /members/<id> - Delete a member

## Design Choices

1. **No External Dependencies**: The project uses only Flask and Python standard library to meet the constraint of avoiding third-party libraries.

2. **Type Safety**: All models and functions use type hints for better code quality and maintainability.

3. **In-Memory Storage**: Data is stored in memory using Python dictionaries for simplicity. In a production environment, this should be replaced with a proper database.

4. **Token-Based Authentication**: Implements a simple token-based authentication system using Python's built-in libraries.

5. **Modular Structure**: Code is organized into modules (models, routes, utils) for better maintainability and testing.

## Assumptions and Limitations

1. **Data Persistence**: Data is stored in memory and will be lost when the server restarts.

2. **Authentication**: Uses a simple token-based system. For production, a more robust solution would be needed.

3. **Concurrency**: The in-memory storage might have race conditions under heavy concurrent access.

4. **Search**: Implements basic string matching. For production, a more sophisticated search solution would be needed.

## Running Tests

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
