from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import SeasonModel
from schemas import SeasonSchema


blp = Blueprint("Seasons", "seasons", description="Operations on seasons")


@blp.route("/seasons/<int:season_id>")
class Season(MethodView):
    @jwt_required()
    @blp.response(200, SeasonSchema)
    def get(self, season_id):
        season = SeasonModel.query.get_or_404(season_id)
        return season
    
    @jwt_required()
    def delete(self, season_id):
        season = SeasonModel.query.get_or_404(season_id)
        db.session.delete(season)
        db.session.commit()
        return {"message": "Season deleted"}, 200


@blp.route("/season")
class SeasonList(MethodView):
    @jwt_required()
    @blp.response(200, SeasonSchema(many=True))
    def get(self):
        return SeasonModel.query.all()

    @jwt_required()
    @blp.arguments(SeasonSchema)
    @blp.response(201, SeasonSchema)
    def post(self, season_data):
        season = SeasonModel(**season_data)
        try:
            db.session.add(season)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the season.")

        return season