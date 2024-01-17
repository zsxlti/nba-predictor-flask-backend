from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from datetime import datetime
from statistics import mean

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
    
@blp.route("/api/game/stats/comparison/<int:team_id>/<string:start_date>/<string:end_date>")
class getGamesComparisonStats(MethodView):
    def get(self, team_id, start_date, end_date):
        # Dátumok konvertálása datetime típusra
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Lekérdezés a GameModel alapján a kezdő- és végdátumok között egy adott csapatra
        games_stats = GameModel.query.filter(
            ((GameModel.team_id_home == team_id) | (GameModel.team_id_away == team_id)) &
            (GameModel.date >= start_date) & (GameModel.date <= end_date)
        ).all()


        # Aggregálás a statisztikai adatokon
        total_pts = sum(game.pts_home if game.team_id_home == team_id else game.pts_away for game in games_stats)
        total_ast = sum(game.ast_home if game.team_id_home == team_id else game.ast_away for game in games_stats)
        total_reb = sum(game.reb_home if game.team_id_home == team_id else game.reb_away for game in games_stats)
        total_dreb = sum(game.dreb_home if game.team_id_home == team_id else game.dreb_away for game in games_stats)
        total_oreb = sum(game.oreb_home if game.team_id_home == team_id else game.oreb_away for game in games_stats)
        total_stl = sum(game.stl_home if game.team_id_home == team_id else game.stl_away for game in games_stats)
        total_blk = sum(game.blk_home if game.team_id_home == team_id else game.blk_away for game in games_stats)
        total_tov = sum(game.tov_home if game.team_id_home == team_id else game.tov_away for game in games_stats)
        total_pf = sum(game.pf_home if game.team_id_home == team_id else game.pf_away for game in games_stats)
        total_fga = sum(game.fga_home if game.team_id_home == team_id else game.fga_away for game in games_stats)
        total_fgm = sum(game.fgm_home if game.team_id_home == team_id else game.fgm_away for game in games_stats)
        total_fg3a = sum(game.fg3a_home if game.team_id_home == team_id else game.fg3a_away for game in games_stats)
        total_fg3m = sum(game.fg3m_home if game.team_id_home == team_id else game.fg3m_away for game in games_stats)
        total_fta = sum(game.fta_home if game.team_id_home == team_id else game.fta_away for game in games_stats)
        total_ftm = sum(game.ftm_home if game.team_id_home == team_id else game.ftm_away for game in games_stats)
        
        
        # További aggregációs műveletek...

        # Az eredmények átalakítása JSON formátumba
        result = {
            "total_pts": total_pts,
            "total_ast": total_ast,
            "total_reb": total_reb,
            "total_dreb": total_dreb,
            "total_oreb": total_oreb,
            "total_stl": total_stl,
            "total_blk": total_blk,
            "total_tov": total_tov,
            "total_pf": total_pf,
            "total_fga": total_fga,
            "total_fgm": total_fgm,
            "total_fg3a": total_fg3a,
            "total_fg3m": total_fg3m,
            "total_fta": total_fta,
            "total_ftm": total_ftm,
            
            "avg_fg_pct": mean(game.fg_pct_home if game.team_id_home == team_id else game.fg_pct_away for game in games_stats),
            "avg_fg3_pct": mean(game.fg3_pct_home if game.team_id_home == team_id else game.fg3_pct_away for game in games_stats),
            "avg_ft_pct": mean(game.ft_pct_home if game.team_id_home == team_id else game.ft_pct_away for game in games_stats),
            # További aggregált adatok...
        }
       
        return jsonify(result)