from flask import Flask, jsonify, render_template
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
    """

    # SQL pentru a adăuga datele inițiale
    insert_data_sql = """
    INSERT INTO movies (title, director, year)
    VALUES 
        ('The Shawshank Redemption', 'Frank Darabont', 1994),
        ('The Dark Knight', 'Christopher Nolan', 2008)
    ON CONFLICT (title) DO NOTHING;
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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
