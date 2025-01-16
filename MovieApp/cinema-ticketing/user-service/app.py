from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
# from routess.userroutes import userRoutes
# from models import db
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, Client

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
            session['user_id'] = user.id
            return jsonify({"message": "Logare cu succes!"}), 200
        else:
            return jsonify({"error": "Username sau parolă invalidă"}), 401

    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)#, host="0.0.0.0", port=8000)
