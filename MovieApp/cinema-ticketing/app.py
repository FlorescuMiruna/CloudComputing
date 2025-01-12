from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, Cinema Ticketing App!"

@app.route('/movies')
def get_movies():
    # Conectare la PostgreSQL
    conn = psycopg2.connect(
        dbname="cinema_db",
        user="postgres",
        password="test-password",
        host="postgres"  # Acesta este numele serviciului din Docker Compose
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    movies = cur.fetchall()
    cur.close()
    conn.close()

    # Returnează rezultatele ca JSON
    return jsonify(movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
