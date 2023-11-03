from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import GameModel
from schemas import GameSchema


blp = Blueprint("Games", "games", description="Operations on games")


@blp.route("/games/<int:game_id>")
class Game(MethodView):
    @jwt_required()
    @blp.response(200, GameSchema)
    def get(self, game_id):
        game = GameModel.query.get_or_404(game_id)
        return game
    
    @jwt_required()
    def delete(self, game_id):
        game = GameModel.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return {"message": "Game deleted"}, 200


@blp.route("/game")
class GameList(MethodView):
    @jwt_required()
    @blp.response(200, GameSchema(many=True))
    def get(self):
        return GameModel.query.all()

    @jwt_required()
    @blp.arguments(GameSchema)
    @blp.response(201, GameSchema)
    def post(self, game_data):
        game = GameModel(**game_data)
        try:
            db.session.add(game)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the game.")

        return game