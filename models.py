from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Observation(db.Model):  # US-10
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    timezone = db.Column(db.String(10), nullable=False)
    coordinates = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wind = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    haze = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
