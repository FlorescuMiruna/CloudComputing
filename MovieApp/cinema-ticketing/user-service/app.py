from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
# from routess.userroutes import userRoutes
# from models import db
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, Client
import jwt
import datetime

app = Flask(__name__)

# session configuration
app.secret_key = 'flask_secret_key'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test-password@user_db_cinema:5432/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'my_secret_key'



# db = SQLAlchemy(app)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import routess


# app = Flask(__name__)
# app.register_blueprint(userRoutes)

SECRET_KEY = 'your-secret-key'

def generate_token(client_id):
    """Generate a JWT token."""
    payload = {
        'client_id': client_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiry (1 day)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


from functools import wraps
from flask import request, jsonify
import jwt


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')  # Fetch the token from the cookie

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify the token (assuming you're using 'secret_key' to encode/decode)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.client_id = data['client_id']  # Attach the client_id to the request object
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Nu ești autentificat"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Route: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        try:
            # Create and add new user
            new_client = Client(username=username, email=email, password_hash=password_hash)
            db.session.add(new_client)
            db.session.commit()
            return jsonify({"message": "Înregistrare cu succes!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    return render_template('register.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query user by username
        user = Client.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            token = generate_token(user.id)
            response = make_response(jsonify({"message": "Logare cu succes!", "token" : token }), 200)
            response.set_cookie('access_token', token, httponly=True, secure=True, samesite='Strict')  # set cookie
            return response
        else:
            return jsonify({"error": "Username sau parolă invalidă"}), 401

    return render_template('login.html')

# Route: Logout
@app.route('/logout', methods=['POST'])
@token_required  # Ensure the user is authenticated (assuming you have a decorator to verify the token)
def logout():
    # Remove the JWT token from the response (client-side)
    response = jsonify({"message": "Logged out successfully"})

    # Remove JWT token from cookies
    response.set_cookie('access_token', '', expires=0)  # Expire the token cookie immediately

    return response

@app.route('/profile', methods=['GET'])
@token_required  # Ensure the user is authenticated (assuming you have a decorator to verify the token)
def profile():
    return render_template('logout.html')

# Endpoint to check if a user exists by ID
@app.route('/users/<int:client_id>', methods=['GET'])
def check_user_by_id(client_id):
    # Query the database for the user by client_id
    user = Client.query.get(client_id)

    # If user exists, return user details
    if user:
        return jsonify({
            'client_id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 200  # HTTP status code 200 for OK
    else:
        return jsonify({'error': 'User not found'}), 404  # HTTP status code 404 for Not Found


@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if client:
        return jsonify(client)
    else:
        return jsonify({'error': 'Client not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)#, host="0.0.0.0", port=8000)
