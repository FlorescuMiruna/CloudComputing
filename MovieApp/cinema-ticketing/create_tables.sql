CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
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

-- CREATE TABLE IF NOT EXISTS employees (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL,
--     salary INT NOT NULL,
--     loyalty_points INT NOT NULL,
--     FOREIGN KEY (id_cinema) REFERENCES cinemas (id) ON DELETE CASCADE ON UPDATE CASCADE
-- );

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


INSERT INTO movies (id, title, director, year)
VALUES (1, 'The Shawshank Redemption', 'Frank Darabont', 1994),
       (2, 'The Dark Knight', 'Christopher Nolan', 2008);

INSERT INTO cinemas (id, name, city, seat_number)
VALUES (1, 'Cinema City PSC Ploiesti', 'Ploiesti', 150),
       (2, 'Cinema City Afi Ploiesti', 'Ploiesti', 100);

INSERT INTO broadcast (movie_id, cinema_id, broadcast_date)
VALUES
    (1, 1, '2025-01-14'),
    (2, 2, '2025-01-15');
