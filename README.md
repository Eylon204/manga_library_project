# Manga Library Management System

A simple library management system for managing books, customers, and loans, built using Flask and SQLAlchemy.

## Project Structure
Manga_Library/
│
├── backend/                  # Backend code
│   ├── app.py                # Main application file
│   ├── app.log               # Log file
│   ├── venv/                 # Virtual environment
│   ├── database.py           # Database connection and configuration
│   ├── models.py             # Database models
│   ├── requirements.txt       # Project dependencies
│   ├── instance/             # Database files
│   │   └── library.db        # SQLite database
│   │
│   ├── routes/               # Route files
│   │   ├── init.py       # Initialize routes
│   │   ├── auth.py           # Authentication routes
│   │   ├── books.py          # Book-related routes
│   │   ├── customers.py       # Customer-related routes
│   │   └── loans.py          # Loan-related routes
│   │
│   └── tests/                # Test files
│       ├── test_app.py       # Tests for app functionality
│       ├── test_books.py      # Tests for book functionality
│       └── test_customers.py  # Tests for customer functionality
│
└── frontend/                 # Frontend code
├── static/               # Static files (CSS, images)
└── templates/            # HTML templates
├── index.html        # Home page
├── add_book.html     # Add book form
├── add_customer.html  # Add customer form
├── create_loan.html   # Create loan form
└── view_books.html    # View all books

## Requirements

To run this project, you need the following installed:
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login

You can install the required packages using the following command:
	1.	Clone the repository:
    git clone <repository-url>
    cd Manga_Library/backend
    
    2.	Create a virtual environment:
    venv\Scripts\activate

    •	On macOS/Linux:
    source venv/bin/activate
    
    4.	Install the required packages:
    pip install -r requirements.txt

    5.	Run the application:
    python3 app.py
    
    6.	Open your browser and go to http://127.0.0.1:5000.

# Usage

	•	Add new books using the Add a New Book button.
	•	Add new customers using the Add a New Customer button.
	•	Create loans for available books using the Create a New Loan button.
	•	View the collection of books in the View Books section.

## Testing:
You can run the tests by executing:
python -m unittest discover -s tests

# License

This project is licensed under the MIT License. See the LICENSE file for more details:
	•	Project Structure: I organized the files and directories clearly to show how the project is structured.
	•	Requirements: I listed the dependencies required to run the project.
	•	Installation: I explained how to clone the project, set up a virtual environment, and install the dependencies.
	•	Usage: A brief explanation of how to use the management system.
	•	Testing: An explanation of how to run the tests.
