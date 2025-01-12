CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    year INT NOT NULL
);


INSERT INTO movies (title, director, year)
VALUES ('The Shawshank Redemption', 'Frank Darabont', 1994),
       ('The Dark Knight', 'Christopher Nolan', 2008);
