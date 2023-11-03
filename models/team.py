from db import db

class TeamModel(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    abbreviation = db.Column(db.String(3), unique=True, nullable=False)
    year_founded = db.Column(db.Integer, nullable=False)
    has_previous_name = db.Column(db.Boolean)