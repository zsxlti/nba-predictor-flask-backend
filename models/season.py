from db import db

class SeasonModel(db.Model):
    __tablename__ = "seasons"

    id = db.Column(db.Integer, primary_key=True)
    season_number = db.Column(db.Integer, nullable=False)