from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import GameModel
from schemas import GameSchema


blp = Blueprint("Games", "games", description="Operations on games")


@blp.route("/api/games/<int:game_id>")
class Game(MethodView):
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


@blp.route("/api/game")
class GameList(MethodView):
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

@blp.route("/api/game/stats/<int:team_id1>/<int:team_id2>")
class getGamesStatsByTeams(MethodView):
    def get(self, team_id1, team_id2):
        # Lekérdezés a GameModel alapján
        games_stats = GameModel.query.filter(
            ((GameModel.team_id_home == team_id1) & (GameModel.team_id_away == team_id2)) |
            ((GameModel.team_id_home == team_id2) & (GameModel.team_id_away == team_id1))
        ).all()

        # Az eredmények átalakítása JSON formátumba
        result = []
        for game in games_stats:
            result.append({
                "id": game.id,
                "season_id": game.season_id,
                "date": game.date.strftime("%Y-%m-%d"),  # Dátum formázása
                "pts_home": game.pts_home,
                "pts_away": game.pts_away,
                "team_id_home": game.team_id_home,
                "team_id_away": game.team_id_away,
                "ast_home": game.ast_home,
                "ast_away": game.ast_away,
                "reb_home": game.reb_home,
                "reb_away": game.reb_away,
                "stl_home": game.stl_home,
                "stl_away": game.stl_away,
                "blk_home": game.blk_home,
                "blk_away": game.blk_away,
                "tov_home": game.tov_home,
                "tov_away": game.tov_away,
                "pf_home": game.pf_home,
                "pf_away": game.pf_away,
                "fga_home": game.fga_home,
                "fgm_home": game.fgm_home,
                "fga_away": game.fga_away,
                "fgm_away": game.fgm_away,
              
            })

        return jsonify(result)
    
@blp.route("/api/game/stats/<int:team_id1>/<int:team_id2>/<int:season_id>")
class getGamesStatsBySeason(MethodView):
    def get(self, team_id1, team_id2, season_id):
        # Lekérdezés a GameModel alapján
        games_stats = GameModel.query.filter(
            ((GameModel.team_id_home == team_id1) & (GameModel.team_id_away == team_id2) & (GameModel.season_id == season_id)) |
            ((GameModel.team_id_home == team_id2) & (GameModel.team_id_away == team_id1) & (GameModel.season_id == season_id))
        ).all()

        # Az eredmények átalakítása JSON formátumba
        result = []
        for game in games_stats:
            result.append({
                "id": game.id,
                "season_id": game.season_id,
                "date": game.date.strftime("%Y-%m-%d"),  # Dátum formázása
                "pts_home": game.pts_home,
                "pts_away": game.pts_away,
                "team_id_home": game.team_id_home,
                "team_id_away": game.team_id_away,
                "ast_home": game.ast_home,
                "ast_away": game.ast_away,
                "reb_home": game.reb_home,
                "reb_away": game.reb_away,
                "stl_home": game.stl_home,
                "stl_away": game.stl_away,
                "blk_home": game.blk_home,
                "blk_away": game.blk_away,
                "tov_home": game.tov_home,
                "tov_away": game.tov_away,
                "pf_home": game.pf_home,
                "pf_away": game.pf_away,
                "fga_home": game.fga_home,
                "fgm_home": game.fgm_home,
                "fga_away": game.fga_away,
                "fgm_away": game.fgm_away,
                
            })

        return jsonify(result)
    

@blp.route("/api/game/stats/details/<int:team_id1>/<int:team_id2>")
class getGamesDetailedStatsByTeams(MethodView):
    def get(self, team_id1, team_id2):
        # Lekérdezés a GameModel alapján
        games_stats = GameModel.query.filter(
            ((GameModel.team_id_home == team_id1) & (GameModel.team_id_away == team_id2)) |
            ((GameModel.team_id_home == team_id2) & (GameModel.team_id_away == team_id1))
        ).all()

        # Az eredmények átalakítása JSON formátumba
        result = []
        for game in games_stats:
            result.append({
                "game_id": game.id,
                "team_id_home": game.team_id_home,
                "team_id_away": game.team_id_away,
                "pts_home": game.pts_home,
                "pts_away": game.pts_away,
                "ast_home": game.ast_home,
                "ast_away": game.ast_away,
                "reb_home": game.reb_home,
                "reb_away": game.reb_away,
                "stl_home": game.stl_home,
                "stl_away": game.stl_away,
                "blk_home": game.blk_home,
                "blk_away": game.blk_away,
                "tov_home": game.tov_home,
                "tov_away": game.tov_away,
                "pf_home": game.pf_home,
                "pf_away": game.pf_away,
                "fga_home": game.fga_home,
                "fgm_home": game.fgm_home,
                "fga_away": game.fga_away,
                "fgm_away": game.fgm_away,
            })

        return jsonify(result)