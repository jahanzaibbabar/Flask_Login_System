# Import the SQLAlchemy class from Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()

# Define a User model representing the 'app_users' table
class User(db.Model):
    # Set the custom table name for the model
    __tablename__ = 'app_users'
    
    # Define columns for the 'app_users' table
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # Constructor to initialize the User object with provided values
    def __init__(self, username, full_name, password):
        self.full_name = full_name
        self.username = username
        self.password = password
