from flask import Flask, jsonify, request
import psycopg2

# Configurația aplicației
class Config:
    DB_NAME = "cinema"
    DB_USER = "postgres"
    DB_PASSWORD = "test-password"
    DB_HOST = "postgres-db"  # Numele serviciului PostgreSQL definit în docker-compose
    DB_PORT = 5432
    SECRET_KEY = 'flask_secret_key'
    SESSION_TYPE = 'filesystem'

app = Flask(__name__)
app.config.from_object(Config)


# Funcție pentru a obține conexiunea la baza de date
def get_db_connection():
    conn = psycopg2.connect(
        dbname=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT']
    )
    return conn


# GET: Obține toate filmele
@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(movies)


# POST: Adaugă un film
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    title = data['title']
    director = data['director']
    year = data['year']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO movies (title, director, year) VALUES (%s, %s, %s) RETURNING id;",
                (title, director, year))
    new_movie_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_movie_id, "title": title, "director": director, "year": year}), 201


# GET: Obține toate cinematografele
@app.route('/cinemas', methods=['GET'])
def get_cinemas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cinemas;")
    cinemas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(cinemas)


# POST: Adaugă un cinema
@app.route('/cinemas', methods=['POST'])
def add_cinema():
    data = request.get_json()
    name = data['name']
    city = data['city']
    seat_number = data['seat_number']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO cinemas (name, city, seat_number) VALUES (%s, %s, %s) RETURNING id;",
                (name, city, seat_number))
    new_cinema_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_cinema_id, "name": name, "city": city, "seat_number": seat_number}), 201


# POST: Adaugă o proiecție
@app.route('/broadcast', methods=['POST'])
def add_broadcast():
    data = request.get_json()
    movie_id = data['movie_id']
    cinema_id = data['cinema_id']
    broadcast_date = data['broadcast_date']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO broadcast (movie_id, cinema_id, broadcast_date) 
        VALUES (%s, %s, %s) RETURNING movie_id, cinema_id, broadcast_date;
    """, (movie_id, cinema_id, broadcast_date))

    inserted_movie_id, inserted_cinema_id, inserted_broadcast_date = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "movie_id": inserted_movie_id,
        "cinema_id": inserted_cinema_id,
        "broadcast_date": inserted_broadcast_date
    }), 201


# GET: Obține toate proiecțiile
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

    return jsonify(broadcasts)


# Testare conexiune cu baza de date
@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"


# Funcție pentru inițializarea bazei de date
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Crearea tabelelor
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL UNIQUE,
        director VARCHAR(255) NOT NULL,
        year INT NOT NULL
    );
    """)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)