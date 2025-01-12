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

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    loyalty_points INT NOT NULL,
    FOREIGN KEY (id_cinema) REFERENCES cinema (id) ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO movies (title, director, year)
VALUES ('The Shawshank Redemption', 'Frank Darabont', 1994),
       ('The Dark Knight', 'Christopher Nolan', 2008);

INSERT INTO cinemas (name, city, seat_number)
VALUES ('Cinema City PSC Ploiesti', 'Ploiesti', 150),
        ('Cinema City Afi Ploiesti', 'Ploiesti', 100);
