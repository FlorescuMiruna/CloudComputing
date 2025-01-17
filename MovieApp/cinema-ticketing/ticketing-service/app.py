import requests
from models import db
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from functools import wraps
import jwt
from models import Ticket


SECRET_KEY = 'your-secret-key'

USER_SERVICE_URL = "http://user-microservices:8000"
CINEMA_SERVICE_URL = "http://cinema-microservices:8000"

app = Flask(__name__)
app.secret_key = 'flask_secret_key'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test-password@ticket_db_cinema:5432/ticket_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'my_secret_key'

db.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            client_id = data['client_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        request.client_id = client_id
        return f(*args, **kwargs)

    return decorated_function


def verify_user_exists(client_id):
    response = requests.get(f"{USER_SERVICE_URL}/users/{client_id}")
    if response.status_code == 200:
        return True
    return False


# @app.route('/book_ticket', methods=['GET', 'POST'])
# @token_required
# def book_ticket():
#     if request.method == 'POST':
#         movie_id = request.form.get('movie_id')
#         cinema_id = request.form.get('cinema_id')
#         seat_nr = request.form.get('seat_nr')
#
#         user_id = request.client_id
#
#         if not verify_user_exists(user_id):
#             flash('Clientul din token nu a putut fi găsit!.', 'danger')
#             return redirect(url_for('login'))
#
#         existing_ticket = Ticket.query.filter_by(movie_id=movie_id, cinema_id=cinema_id, seat_nr=seat_nr).first()
#
#         if existing_ticket:
#             flash('Acest loc este deja rezervat! Vă rugăm alegeți altul.', 'danger')
#         else:
#             new_ticket = Ticket(client_id=user_id, movie_id=movie_id, cinema_id=cinema_id, seat_nr=seat_nr)
#             db.session.add(new_ticket)
#             db.session.commit()
#             flash('Bilet rezervat cu succes!', 'success')
#
#             return redirect(url_for('view_tickets'))
#
#     return render_template('book_ticket.html')

@app.route('/book_ticket', methods=['GET', 'POST'])
@token_required
def book_ticket():
    if request.method == 'POST':
        # Retrieve data from the form
        movie_id = request.form.get('movie_id')
        cinema_id = request.form.get('cinema_id')
        seat_nr = request.form.get('seat_nr')

        # Verify if the seat is already booked
        existing_ticket = Ticket.query.filter_by(
            movie_id=movie_id,
            cinema_id=cinema_id,
            seat_nr=seat_nr
        ).first()

        if existing_ticket:
            flash('Acest loc este deja rezervat! Vă rugăm alegeți altul.', 'danger')
        else:
            # Add a new ticket to the database
            new_ticket = Ticket(
                client_id=request.client_id,  # Assuming the user's ID is stored in the session
                movie_id=movie_id,
                cinema_id=cinema_id,
                seat_nr=seat_nr
            )
            db.session.add(new_ticket)
            db.session.commit()

            flash('Bilet rezervat cu succes!', 'success')
            return redirect(url_for('view_tickets'))

    # Fetch movies from the cinema microservice
    try:
        response = requests.get(f"{CINEMA_SERVICE_URL}/get_movies")
        response.raise_for_status()
        movies = response.json()
    # except requests.RequestException:
    #     flash('Eroare la conectarea cu serviciul de cinematograf.', 'danger')
    #     movies = []
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the cinema service.")
        return {"error": "Failed to connect to the cinema service."}
    except requests.exceptions.Timeout:
        print("The request to the cinema service timed out.")
        return {"error": "The request to the cinema service timed out."}
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return {"error": f"HTTP error occurred: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

    return render_template('book_ticket.html', movies=movies)

@app.route('/cinemas_by_movie')
def get_cinemas_for_movie():
    movie_id = request.args.get('movie_id')
    if not movie_id:
        return jsonify([])

    try:
        response = requests.get(f"{CINEMA_SERVICE_URL}/cinemas_by_movie?movie_id={movie_id}")
        response.raise_for_status()
        cinemas = response.json()
    except requests.RequestException:
        return jsonify([])

    return jsonify(cinemas)


@app.route('/tickets')
@token_required
def view_tickets():
    user_id = request.client_id

    if not verify_user_exists(user_id):
        flash('Clientul din token nu a putut fi găsit!.', 'danger')
        return redirect(url_for('login'))

    tickets = Ticket.query.filter_by(client_id=user_id).all()

    ticket_details = []
    for ticket in tickets:
        ticket_details.append({
            'movie_id': ticket.movie_id,
            'cinema_id': ticket.cinema_id,
            'seat_nr': ticket.seat_nr
        })

    return render_template('tickets.html', tickets=ticket_details)
