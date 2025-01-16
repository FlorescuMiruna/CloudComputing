CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    client_id SERIAL NOT NULL,
    movie_id SERIAL NOT NULL,
    cinema_id SERIAL NOT NULL,
    seat_nr VARCHAR(10) NOT NULL--,
--     FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE,
--     FOREIGN KEY (movie_id, cinema_id) REFERENCES broadcast (movie_id, cinema_id) ON DELETE CASCADE,
--     CONSTRAINT fk_broadcast UNIQUE (movie_id, cinema_id, seat_nr)  -- Ensure unique seat for a given broadcast
);