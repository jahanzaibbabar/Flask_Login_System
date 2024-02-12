# Import necessary modules and classes from Flask and models
from flask import Flask, url_for, render_template, request, redirect, session
from models import db, User

# Create a Flask application
app = Flask(__name__)

# Set a secret key for session management (change this to a more secure value, not so important yet)
app.config['SECRET_KEY'] = 'dfvjh334gjhv$gjhjh'

# Configure the database URI for PostgreSQL 
# REPLACE USERNAME and PASSWORD WITH YOUR DB USERNAME and PASSWORD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/ewsmetrics'

# Disable Flask-SQLAlchemy modification tracking, as it is not necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Flask-SQLAlchemy extension with the app
db.init_app(app)

# Create all database tables (if they do not exist) within the application context
with app.app_context():
    db.create_all()

# Define a route for the home page
@app.route('/', methods=['GET'])
def index():
    # Check if the user is logged in
    if session.get('logged_in'):
        # Retrieve the user object from the database based on the username stored in the session
        user = User.query.filter_by(username=session['username']).first().full_name
        # Render the home template and pass the user's full name
        return render_template('home.html', user=user)
    else:
        # If not logged in, render the index template with a welcome message
        return render_template('index.html', message="Hello!")

# Define a route for user registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        try:
            # Create a new user object with data from the registration form
            new_user = User(full_name=request.form['full_name'], username=request.form['username'], password=request.form['password'])
            # Add the new user to the database
            db.session.add(new_user)
            # Commit the changes to the database
            db.session.commit()
            # Redirect to the login page after successful registration
            return redirect(url_for('login'))
        except:
            # If an exception occurs (user already exists), render the registration template with an error message
            return render_template('register.html', message="User Already Exists")
    else:
        # If the request method is GET, render the registration template
        return render_template('register.html')

# Define a route for user login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Retrieve the username and password from the login form
        u = request.form['username']
        p = request.form['password']
        # Query the database for a user with the provided username and password
        data = User.query.filter_by(username=u, password=p).first()
        # Check if a user with the given credentials exists
        if data is not None:
            # If yes, set the 'logged_in' session variable to True and store the username in the session
            session['logged_in'] = True
            session['username'] = u
            # Redirect to the home page after successful login
            return redirect(url_for('index'))
        # If no user found with the provided credentials, render the login template with an error message
        return render_template('login.html', message="Incorrect Details")
    else:
        # If the request method is GET, render the login template
        return render_template('login.html')

# Define a route for user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Set the 'logged_in' session variable to False and remove the 'username' from the session
    session['logged_in'] = False
    session.pop('username', None)
    # Redirect to the home page after successful logout
    return redirect(url_for('index'))

# Run the application if it is the main module
if __name__ == '__main__':
    app.run()
