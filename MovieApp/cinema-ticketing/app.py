from flask import Flask, jsonify, render_template, request
import psycopg2
from psycopg2 import sql

app = Flask(__name__)


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
        PRIMARY KEY (movie_id, cinema_id),
        FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
        FOREIGN KEY (cinema_id) REFERENCES cinemas (id) ON DELETE CASCADE
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
        
    INSERT INTO broadcast (movie_id, cinema_id)
    VALUES (1, 1),
           (2, 2);
    """

    # Executăm crearea tabelei și adăugarea datelor
    cur.execute(create_table_sql)
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

    # Creează o conexiune la baza de date și execută insert ul
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO broadcast (movie_id, cinema_id) VALUES (%s, %s) RETURNING movie_id, cinema_id;",
        (movie_id, cinema_id)
    )

    inserted_movie_id, inserted_cinema_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "movie_id": inserted_movie_id,
        "cinema_id": inserted_cinema_id
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
        SELECT cinemas.id, cinemas.name, cinemas.city, movies.title 
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

        # Grupam filmele dupa cinema
        if cinema_id not in cinemas_movies:
            cinemas_movies[cinema_id] = {
                'name': cinema_name,
                'city': cinema_city,
                'movies': []
            }

        cinemas_movies[cinema_id]['movies'].append(movie_title)

    return render_template('broadcasts.html', cinemas_movies=cinemas_movies)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
