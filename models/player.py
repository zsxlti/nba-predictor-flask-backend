from db import db

class PlayerModel(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    jersey = db.Column(db.Integer)
    position = db.Column(db.String(255))

    team_id = db.Column(db.Integer, nullable=False)

    from_year = db.Column(db.Integer)
    to_year = db.Column(db.Integer)