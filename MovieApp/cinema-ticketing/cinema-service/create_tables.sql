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

INSERT INTO movies (title, director, year)
    VALUES
        ('The Shawshank Redemption', 'Frank Darabont', 1994),
        ('The Dark Knight', 'Christopher Nolan', 2008)
    ON CONFLICT (title) DO NOTHING;

INSERT INTO cinemas (name, city, seat_number)
VALUES
    ('Cinema City PSC Ploiesti', 'Ploiesti', 150),
    ('Cinema City Afi Ploiesti', 'Ploiesti', 100);

INSERT INTO broadcast (movie_id, cinema_id, broadcast_date)
VALUES
    (1, 1, '2025-01-14'),
    (2, 2, '2025-01-15');