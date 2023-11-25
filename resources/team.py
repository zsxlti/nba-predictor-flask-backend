from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import TeamModel
from schemas import TeamSchema


blp = Blueprint("Teams", "teams", description="Operations on teams")


@blp.route("/api/team/<int:team_id>")
class Team(MethodView):
    @jwt_required()
    @blp.response(200, TeamSchema)
    def get(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        return team
    
    @jwt_required()
    def delete(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return {"message": "Team deleted"}, 200


@blp.route("/api/team")
class TeamList(MethodView):
    @blp.response(200)
    def get(self):
        teams = TeamModel.query.all()
        team_names = [team.name for team in teams]  # Csapatnevek listája
        return team_names

    @jwt_required()
    @blp.arguments(TeamSchema)
    @blp.response(201, TeamSchema)
    def post(self, team_data):
        team = TeamModel(**team_data)
        try:
            db.session.add(team)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A team with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the team.")

        return team