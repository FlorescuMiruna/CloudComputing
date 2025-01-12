from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, Cinema Ticketing App!"

@app.route('/test_db')
def test_db():
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
@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    movies = cur.fetchall()
    cur.close()
    conn.close()

    # Returnează filmele ca JSON
    return jsonify(movies)

# # GET: Pentru a obține un film după ID
# @app.route('/movies/<int:movie_id>', methods=['GET'])
# def get_movie(movie_id):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM movies WHERE id = %s;", (movie_id,))
#     movie = cur.fetchone()
#     cur.close()
#     conn.close()
#
#     if movie:
#         return jsonify(movie)
#     else:
#         return jsonify({"error": "Movie not found"}), 404
#
# # POST: Pentru a adăuga un film nou
# @app.route('/movies', methods=['POST'])
# def post_movie():
#     new_movie = request.get_json()
#
#     title = new_movie['title']
#     director = new_movie['director']
#     year = new_movie['year']
#
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO movies (title, director, year) VALUES (%s, %s, %s) RETURNING id;",
#         (title, director, year)
#     )
#     new_movie_id = cur.fetchone()[0]
#     conn.commit()
#     cur.close()
#     conn.close()
#
#     return jsonify({"id": new_movie_id, "title": title, "director": director, "year": year}), 201
#
# # PUT: Pentru a actualiza un film existent
# @app.route('/movies/<int:movie_id>', methods=['PUT'])
# def put_movie(movie_id):
#     updated_movie = request.get_json()
#
#     title = updated_movie.get('title')
#     director = updated_movie.get('director')
#     year = updated_movie.get('year')
#
#     conn = get_db_connection()
#     cur = conn.cursor()
#
#     # Verificăm dacă filmul există
#     cur.execute("SELECT * FROM movies WHERE id = %s;", (movie_id,))
#     movie = cur.fetchone()
#
#     if not movie:
#         cur.close()
#         conn.close()
#         return jsonify({"error": "Movie not found"}), 404
#
#     # Actualizăm filmul
#     update_query = sql.SQL(
#         "UPDATE movies SET title = %s, director = %s, year = %s WHERE id = %s;"
#     )
#     cur.execute(update_query, (title, director, year, movie_id))
#     conn.commit()
#
#     cur.close()
#     conn.close()

    return jsonify({"id": movie_id, "title": title, "director": director, "year": year}), 200

# DELETE: Pentru a șterge un film după ID
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Verificăm dacă filmul există
    cur.execute("SELECT * FROM movies WHERE id = %s;", (movie_id,))
    movie = cur.fetchone()

    if not movie:
        cur.close()
        conn.close()
        return jsonify({"error": "Movie not found"}), 404

    # Ștergem filmul
    cur.execute("DELETE FROM movies WHERE id = %s;", (movie_id,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Movie deleted successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
