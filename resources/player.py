from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import PlayerModel
from schemas import PlayerSchema, PlayerUpdateSchema

blp = Blueprint("Players", "players", description="Operations on players")


@blp.route("/api/player/<int:player_id>")
class Player(MethodView):
    @jwt_required()
    @blp.response(200, PlayerSchema)
    def get(self, player_id):
        player = PlayerModel.query.get_or_404(player_id)
        return player
    
    @jwt_required()
    def delete(self, player_id):
        player = PlayerModel.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()
        return {"message": "Player deleted."}


    @blp.arguments(PlayerUpdateSchema)
    @blp.response(200, PlayerSchema)
    def put(self, player_data, player_id):
        player = PlayerModel.query.get(player_id)

        if player:
            player.first_name= player_data["first_name"]
            player.last_name= player_data["last_name"]
            player.country= player_data["country"]
            player.jersey= player_data["jersey"]
            player.position= player_data["position"]
            player.from_year= player_data["from_year"]
            player.to_year= player_data["to_year"]
        else:
            player = PlayerModel(id=player_id, **player_data)
        
        db.session.add(player)
        db.session.commit()

        return player


@blp.route("/api/player")
class PlayerList(MethodView):
    @jwt_required()
    @blp.response(200, PlayerSchema(many=True))
    def get(self):
        return PlayerModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(PlayerSchema)
    @blp.response(201, PlayerSchema)
    def post(self, player_data):
        player = PlayerModel(**player_data)

        try:
            db.session.add(player)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the player.")

        return player