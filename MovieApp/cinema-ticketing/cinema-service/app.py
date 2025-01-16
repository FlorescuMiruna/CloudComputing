from flask import Flask, jsonify, render_template, request, redirect, flash, url_for
import psycopg2
from psycopg2 import sql

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session

from functools import wraps

app = Flask(__name__)

# session configuration
app.secret_key = 'flask_secret_key'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


# Funcție pentru a crea tabelele și a adăuga datele inițiale
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # SQL pentru crearea tabelelor
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL UNIQUE,
        director VARCHAR(255) NOT NULL,
        year INT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS cinemas (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        seat_number INT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS broadcast (
        movie_id SERIAL NOT NULL,
        cinema_id SERIAL NOT NULL,
        broadcast_date DATE NOT NULL,
        PRIMARY KEY (movie_id, cinema_id),
        FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
        FOREIGN KEY (cinema_id) REFERENCES cinemas (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS clients (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS tickets (
        id SERIAL PRIMARY KEY,
        client_id SERIAL NOT NULL,
        movie_id SERIAL NOT NULL,
        cinema_id SERIAL NOT NULL,
        seat_nr VARCHAR(10) NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id, cinema_id) REFERENCES broadcast (movie_id, cinema_id) ON DELETE CASCADE,
        CONSTRAINT fk_broadcast UNIQUE (movie_id, cinema_id, seat_nr)  -- Ensure unique seat for a given broadcast
    );
    """

    # SQL pentru a adăuga datele inițiale
    insert_data_sql = """
    INSERT INTO movies (id, title, director, year)
    VALUES
        (1, 'The Shawshank Redemption', 'Frank Darabont', 1994),
        (2, 'The Dark Knight', 'Christopher Nolan', 2008)
    ON CONFLICT (title) DO NOTHING;

    INSERT INTO cinemas (id, name, city, seat_number)
    VALUES
        (1, 'Cinema City PSC Ploiesti', 'Ploiesti', 150),
        (2, 'Cinema City Afi Ploiesti', 'Ploiesti', 100);

    INSERT INTO broadcast (movie_id, cinema_id, broadcast_date)
    VALUES
        (1, 1, '2025-01-14'),
        (2, 2, '2025-01-15');
    """

    # SQL pentru a adauga user admin/ password
    insert_admin_user = """
    INSERT INTO clients (username, email, password_hash)
    VALUES (%s, %s, %s);
    """

    # Executăm crearea tabelei și adăugarea datelor
    cur.execute(create_table_sql)

    hashed_password = generate_password_hash("password")
    # Insert admin user
    try:
        cur.execute(insert_admin_user, ('admin', 'admin@example.com', hashed_password))
        conn.commit()
        print("Admin user added successfully.")
    except Exception as e:
        print("Error adding admin user:", e)

    cur.execute(insert_data_sql)
    conn.commit()
    cur.close()
    conn.close()

# Apelăm funcția de inițializare a bazei de date când aplicația pornește
# @app.before_first_request
# def before_first_request():
#     init_db()

@app.route('/')
def hello_world():
    return "Hello, Cinema Ticketing App!"

@app.route('/test_db')
def test_db():
    init_db()
    try:
        conn = get_db_connection()
        conn.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

# Funcție pentru a obține conexiunea la baza de date
def get_db_connection():
    conn = psycopg2.connect(
        dbname="cinema_db",
        user="postgres",
        password="test-password",
        host="postgres-db",  # Aici folosești numele containerului PostgreSQL
        port=5432
    )
    return conn
# GET: Pentru a obține toate filmele
# @app.route('/movies', methods=['GET'])
# def get_movies():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM movies;")
#     movies = cur.fetchall()
#     cur.close()
#     conn.close()
#     return jsonify(movies)

# GET: Pentru a obține toate filmele
@app.route('/movies')
def get_movies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")  # Aici selectăm toate filmele
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('movies.html', movies=movies)


# POST: Pentru a adăuga un film nou
@app.route('/movies', methods=['POST'])
def post_movie():
    # Obține datele trimise din formularul HTML
    new_movie = request.form

    # Extrage valorile
    title = new_movie['title']
    director = new_movie['director']
    year = new_movie['year']

    # Creează o conexiune la baza de date și execută interogarea
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO movies (title, director, year) VALUES (%s, %s, %s) RETURNING id;",
        (title, director, year)
    )
    new_movie_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_movie_id, "title": title, "director": director, "year": year}), 201


@app.route('/add_movie')
def add_movie():
    return render_template('add_movie.html')

# GET: Pentru a obtine toate cinema-urile
@app.route('/cinemas')
def get_cinemas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cinemas;")
    cinemas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('cinemas.html', cinemas=cinemas)

# POST: Pentru a adauga un cinema nou
@app.route('/cinemas', methods=['POST'])
def post_cinema():
    # Obține datele trimise din formularul HTML
    new_cinema = request.form

    # Extrage valorile
    name = new_cinema['name']
    city = new_cinema['city']
    seat_number = new_cinema['seat_number']

    # Creează o conexiune la baza de date și execută insert ul
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cinemas (name, city, seat_number) VALUES (%s, %s, %s) RETURNING id;",
        (name, city, seat_number)
    )
    new_cinema_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_cinema_id, "name": name, "city": city, "seat_number": seat_number}), 201

@app.route('/add_cinema')
def add_cinema():
    return render_template('add_cinema.html')

# POST: Pentru a adauga o noua proiectie
@app.route('/broadcast', methods=['POST'])
def post_broadcast():
    # Obține datele trimise din formularul HTML
    new_broadcast = request.form

    # Extrage valorile
    movie_id = new_broadcast['movie_id']
    cinema_id = new_broadcast['cinema_id']
    broadcast_date = new_broadcast['broadcast_date']

    # Creează o conexiune la baza de date și execută insert ul
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO broadcast (movie_id, cinema_id, broadcast_date) "
        "VALUES (%s, %s, %s) RETURNING movie_id, cinema_id, broadcast_date;",
        (movie_id, cinema_id, broadcast_date)
    )

    inserted_movie_id, inserted_cinema_id, inserted_broadcast_date = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "movie_id": inserted_movie_id,
        "cinema_id": inserted_cinema_id,
        "broadcast_date": inserted_broadcast_date
    }), 201


@app.route('/add_broadcast')
def add_broadcast():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM movies;")
    movies = cur.fetchall()

    cur.execute("SELECT * FROM cinemas;")
    cinemas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('add_broadcast.html', movies=movies, cinemas=cinemas)

# GET: Pentru a obține toate proiectiile
@app.route('/broadcasts', methods=['GET'])
def get_broadcasts():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT cinemas.id, cinemas.name, cinemas.city, movies.title, broadcast.broadcast_date
        FROM cinemas
        JOIN broadcast ON cinemas.id = broadcast.cinema_id
        JOIN movies ON broadcast.movie_id = movies.id
        ORDER BY cinemas.name, movies.title;
    """)

    broadcasts = cur.fetchall()

    cur.close()
    conn.close()

    cinemas_movies = {}
    for broadcast in broadcasts:
        cinema_id = broadcast[0]
        cinema_name = broadcast[1]
        cinema_city = broadcast[2]
        movie_title = broadcast[3]
        broadcast_date = broadcast[4]

        # Grupam filmele dupa cinema
        if cinema_id not in cinemas_movies:
            cinemas_movies[cinema_id] = {
                'name': cinema_name,
                'city': cinema_city,
                'movies': []
            }

        cinemas_movies[cinema_id]['movies'].append({
            'title': movie_title,
            'date': broadcast_date
        })

    return render_template('broadcasts.html', cinemas_movies=cinemas_movies)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         password_hash = generate_password_hash(password)
#
#         conn = get_db_connection()
#         cur = conn.cursor()
#
#         try:
#             cur.execute("""
#                 INSERT INTO clients (username, email, password_hash)
#                 VALUES (%s, %s, %s)
#                 RETURNING id;
#             """, (username, email, password_hash))
#             conn.commit()
#             cur.close()
#             conn.close()
#             return jsonify({"message": "Înregistrare cu succes!"}), 201
#         except Exception as e:
#             conn.rollback()
#             cur.close()
#             conn.close()
#             return jsonify({"error": str(e)}), 400
#
#     return render_template('register.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT id, password_hash FROM clients WHERE username = %s;", (username,))
#         user = cur.fetchone()
#         cur.close()
#         conn.close()
#
#         if user and check_password_hash(user[1], password):
#             session['user_id'] = user[0]
#             return jsonify({"message": "Logare cu succes!"}), 200
#         else:
#             return jsonify({"error": "Username sau parolă invalidă"}), 401
#
#     return render_template('login.html')
#
#
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return jsonify({"error": "Nu ești autentificat"}), 401
#         return f(*args, **kwargs)
#     return decorated_function
#
# @app.route('/logout')
# def logout():
#     session.clear()  # Golim datele din sesiunea curenta
#     return redirect(url_for('login'))

@app.route('/get_cinemas_for_movie', methods=['GET'])
def get_cinemas_for_movie():
    movie_id = request.args.get('movie_id', type=int)

    conn = get_db_connection()
    cur = conn.cursor()

    # Obținem cinema urile care proiecteaza filmul selectat
    cur.execute("""
        SELECT cinemas.id, cinemas.name
        FROM cinemas
        JOIN broadcast ON cinemas.id = broadcast.cinema_id
        WHERE broadcast.movie_id = %s;
    """, (movie_id,))

    cinemas = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(cinemas)

@app.route('/book_ticket', methods=['GET', 'POST'])
# @login_required
def book_ticket():
    if request.method == 'POST':
        # Obține datele trimise din formularul HTML
        movie_id = request.form.get('movie_id')
        cinema_id = request.form.get('cinema_id')
        seat_nr = request.form.get('seat_nr')

        # Verificam daca locul este deja rezervat
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 1 FROM tickets
            WHERE movie_id = %s AND cinema_id = %s AND seat_nr = %s;
        """, (movie_id, cinema_id, seat_nr))
        existing_ticket = cur.fetchone()

        if existing_ticket:
            flash('Acest loc este deja rezervat! Vă rugăm alegeți altul.', 'danger')
        else:
            # Inseram un bilet in tabela
            cur.execute("""
                INSERT INTO tickets (client_id, movie_id, cinema_id, seat_nr)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (session['user_id'], movie_id, cinema_id, seat_nr))
            conn.commit()

            flash('Bilet rezervat cu succes!', 'success')

            cur.close()
            conn.close()

            return redirect(url_for('view_tickets'))  # Redirect la pagina de bilete

    # GET: obtinem toate filmele
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title FROM movies ORDER BY title;")
    movies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('book_ticket.html', movies=movies)



@app.route('/tickets')
# @login_required
def view_tickets():
    user_id = session.get('user_id')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            cinemas.name,
            movies.title,
            broadcast.broadcast_date,
            tickets.seat_nr
        FROM tickets
        JOIN broadcast ON tickets.cinema_id = broadcast.cinema_id AND tickets.movie_id = broadcast.movie_id
        JOIN cinemas ON broadcast.cinema_id = cinemas.id
        JOIN movies ON broadcast.movie_id = movies.id
        WHERE tickets.client_id = %s
        ORDER BY broadcast.broadcast_date DESC;
    """, (user_id,))

    tickets = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('tickets.html', tickets=tickets)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
