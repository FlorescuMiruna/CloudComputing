# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
# class Ticket(db.Model):
#     __tablename__ = 'tickets'
#
#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
#     movie_id = db.Column(db.Integer, db.ForeignKey('broadcast.movie_id', ondelete='CASCADE'), nullable=False)
#     cinema_id = db.Column(db.Integer, db.ForeignKey('broadcast.cinema_id', ondelete='CASCADE'), nullable=False)
#     seat_nr = db.Column(db.String(10), nullable=False)
#
#     # Relationships
#     client = db.relationship('Client', backref='tickets', lazy=True)
#     broadcast = db.relationship('Broadcast', backref='tickets', lazy=True)
#
#     # Unique constraint to ensure a unique seat for each movie and cinema
#     __table_args__ = (
#         db.UniqueConstraint('movie_id', 'cinema_id', 'seat_nr', name='fk_broadcast'),
#     )
#
#     def __init__(self, client_id, movie_id, cinema_id, seat_nr):
#         self.client_id = client_id
#         self.movie_id = movie_id
#         self.cinema_id = cinema_id
#         self.seat_nr = seat_nr
#
#     def __repr__(self):
#         return f'<Ticket client_id={self.client_id}, movie_id={self.movie_id}, cinema_id={self.cinema_id}, seat_nr={self.seat_nr}>'
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'client_id': self.client_id,
#             'movie_id': self.movie_id,
#             'cinema_id': self.cinema_id,
#             'seat_nr': self.seat_nr
#         }

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy()

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False) #db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    cinema_id = db.Column(db.Integer, nullable=False)
    seat_nr = db.Column(db.String(10), nullable=False)

    # Relationship with the Client model (one-to-many)
    # client = db.relationship('Client', backref='tickets', lazy=True)



    # Unique constraint to ensure a unique seat for each movie and cinema
    __table_args__ = (
        db.UniqueConstraint('movie_id', 'cinema_id', 'seat_nr', name='fk_broadcast'),
    )

    def __init__(self, client_id, movie_id, cinema_id, seat_nr):
        self.client_id = client_id
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.seat_nr = seat_nr

    def __repr__(self):
        return f'<Ticket client_id={self.client_id}, movie_id={self.movie_id}, cinema_id={self.cinema_id}, seat_nr={self.seat_nr}>'

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'movie_id': self.movie_id,
            'cinema_id': self.cinema_id,
            'seat_nr': self.seat_nr
        }

    def get_client_info(self):
        # Assuming the client service is available at this URL
        client_service_url = f'http://user-microservices:8000/{self.client_id}'
        response = requests.get(client_service_url)
        if response.status_code == 200:
            return response.json()  # returns the client info as a dictionary
        return None
