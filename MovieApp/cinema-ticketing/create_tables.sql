CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS broadcast (
    movie_id SERIAL NOT NULL,
    cinema_id SERIAL NOT NULL,
    PRIMARY KEY (movie_id, cinema_id),
    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
    FOREIGN KEY (cinema_id) REFERENCES cinemas (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cinemas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    seat_number INT NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    loyalty_points INT NOT NULL,
    FOREIGN KEY (id_cinema) REFERENCES cinema (id) ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO movies (id, title, director, year)
VALUES (1, 'The Shawshank Redemption', 'Frank Darabont', 1994),
       (2, 'The Dark Knight', 'Christopher Nolan', 2008);

INSERT INTO cinemas (id, name, city, seat_number)
VALUES (1, 'Cinema City PSC Ploiesti', 'Ploiesti', 150),
       (2, 'Cinema City Afi Ploiesti', 'Ploiesti', 100);

INSERT INTO broadcast (movie_id, cinema_id)
VALUES (1, 1),
       (2, 2);
