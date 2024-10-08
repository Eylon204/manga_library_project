from flask import Flask, render_template
from flask_login import LoginManager
from database import db
from models import User
from routes.auth import auth_bp
from routes.books import book_bp
from routes.loans import loans_bp
from routes.customers import customers_bp

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Setting SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SQLAlchemy
db.init_app(app)

# Initialize login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    with db.session() as session:
        return session.get(User, int(user_id))

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)
app.register_blueprint(loans_bp)
app.register_blueprint(customers_bp)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Form pages
@app.route('/add_book')
def add_book():
    return render_template('add_book.html')

@app.route('/add_customer')
def add_customer():
    return render_template('add_customer.html')

@app.route('/create_loan')
def create_loan():
    return render_template('create_loan.html')

@app.route('/view_books')
def view_books():
    return render_template('view_books.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)