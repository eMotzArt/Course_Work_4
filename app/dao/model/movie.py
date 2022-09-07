from app.database import db

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    genre = db.relationship("Genre", backref=db.backref("used_in_movies"))
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"), nullable=False)
    director = db.relationship("Director", backref=db.backref("used_in_movies"))
