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
     
# @blp.route("/api/game/stats/comparison/<int:team_id>/<string:start_date>/<string:end_date>")
# class getGamesComparisonStats(MethodView):
#     def get(self, team_id, start_date, end_date):
#         # Dátumok konvertálása datetime típusra
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         end_date = datetime.strptime(end_date, "%Y-%m-%d")

#         # Lekérdezés a GameModel alapján a kezdő- és végdátumok között egy adott csapatra
#         games_stats = GameModel.query.filter(
#             ((GameModel.team_id_home == team_id) | (GameModel.team_id_away == team_id)) &
#             (GameModel.date >= start_date) & (GameModel.date <= end_date)
#         ).all()


#         # Aggregálás a statisztikai adatokon
#         total_pts = sum(game.pts_home if game.team_id_home == team_id else game.pts_away for game in games_stats)
#         total_ast = sum(game.ast_home if game.team_id_home == team_id else game.ast_away for game in games_stats)
#         total_reb = sum(game.reb_home if game.team_id_home == team_id else game.reb_away for game in games_stats)
#         total_dreb = sum(game.dreb_home if game.team_id_home == team_id else game.dreb_away for game in games_stats)
#         total_oreb = sum(game.oreb_home if game.team_id_home == team_id else game.oreb_away for game in games_stats)
#         total_stl = sum(game.stl_home if game.team_id_home == team_id else game.stl_away for game in games_stats)
#         total_blk = sum(game.blk_home if game.team_id_home == team_id else game.blk_away for game in games_stats)
#         total_tov = sum(game.tov_home if game.team_id_home == team_id else game.tov_away for game in games_stats)
#         total_pf = sum(game.pf_home if game.team_id_home == team_id else game.pf_away for game in games_stats)
#         total_fga = sum(game.fga_home if game.team_id_home == team_id else game.fga_away for game in games_stats)
#         total_fgm = sum(game.fgm_home if game.team_id_home == team_id else game.fgm_away for game in games_stats)
#         total_fg3a = sum(game.fg3a_home if game.team_id_home == team_id else game.fg3a_away for game in games_stats)
#         total_fg3m = sum(game.fg3m_home if game.team_id_home == team_id else game.fg3m_away for game in games_stats)
#         total_fta = sum(game.fta_home if game.team_id_home == team_id else game.fta_away for game in games_stats)
#         total_ftm = sum(game.ftm_home if game.team_id_home == team_id else game.ftm_away for game in games_stats)
        
        
#         # További aggregációs műveletek...

#         # Az eredmények átalakítása JSON formátumba
#         result = {
#             "total_pts": total_pts,
#             "total_ast": total_ast,
#             "total_reb": total_reb,
#             "total_dreb": total_dreb,
#             "total_oreb": total_oreb,
#             "total_stl": total_stl,
#             "total_blk": total_blk,
#             "total_tov": total_tov,
#             "total_pf": total_pf,
#             "total_fga": total_fga,
#             "total_fgm": total_fgm,
#             "total_fg3a": total_fg3a,
#             "total_fg3m": total_fg3m,
#             "total_fta": total_fta,
#             "total_ftm": total_ftm,
            
#             "avg_fg_pct": mean(game.fg_pct_home if game.team_id_home == team_id else game.fg_pct_away for game in games_stats),
#             "avg_fg3_pct": mean(game.fg3_pct_home if game.team_id_home == team_id else game.fg3_pct_away for game in games_stats),
#             "avg_ft_pct": mean(game.ft_pct_home if game.team_id_home == team_id else game.ft_pct_away for game in games_stats),
#             # További aggregált adatok...
#         }
       
#         return jsonify(result)
    

def safely_convert_to_float(value, default=0.0):
    return float(value) if value is not None else default



@blp.route("/api/game/stats/comparison/<int:team_id_1>/<int:team_id_2>/<string:start_date>/<string:end_date>")
class GetGamesComparisonStats(MethodView):
    def get(self, team_id_1, team_id_2, start_date, end_date):
        # Dátumok konvertálása datetime típusra
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Lekérdezés a GameModel alapján a kezdő- és végdátumok között két csapatra
        games_stats = GameModel.query.filter(
            ((GameModel.team_id_home == team_id_1) | (GameModel.team_id_away == team_id_1) |
             (GameModel.team_id_home == team_id_2) | (GameModel.team_id_away == team_id_2)) &
            (GameModel.date >= start_date) & (GameModel.date <= end_date)
        ).all()

        # Aggregálás a statisztikai adatokon a két csapatra
        total_pts_team_1 = sum(game.pts_home if game.team_id_home == team_id_1 else game.pts_away for game in games_stats)
        total_ast_team_1 = sum(game.ast_home if game.team_id_home == team_id_1 else game.ast_away for game in games_stats)
        total_reb_team_1 = sum(game.reb_home if game.team_id_home == team_id_1 else game.reb_away for game in games_stats)
        total_dreb_team_1 = sum(game.dreb_home if game.team_id_home == team_id_1 else game.dreb_away for game in games_stats)
        total_oreb_team_1 = sum(game.oreb_home if game.team_id_home == team_id_1 else game.oreb_away for game in games_stats)
        total_stl_team_1 = sum(game.stl_home if game.team_id_home == team_id_1 else game.stl_away for game in games_stats)
        total_blk_team_1 = sum(game.blk_home if game.team_id_home == team_id_1 else game.blk_away for game in games_stats)
        total_tov_team_1 = sum(game.tov_home if game.team_id_home == team_id_1 else game.tov_away for game in games_stats)
        total_pf_team_1 = sum(game.pf_home if game.team_id_home == team_id_1 else game.pf_away for game in games_stats)
        total_fga_team_1 = sum(game.fga_home if game.team_id_home == team_id_1 else game.fga_away for game in games_stats)
        total_fgm_team_1 = sum(game.fgm_home if game.team_id_home == team_id_1 else game.fgm_away for game in games_stats)
        total_fg3a_team_1 = sum(game.fg3a_home if game.team_id_home == team_id_1 else game.fg3a_away for game in games_stats)
        total_fg3m_team_1 = sum(game.fg3m_home if game.team_id_home == team_id_1 else game.fg3m_away for game in games_stats)
        total_fta_team_1 = sum(game.fta_home if game.team_id_home == team_id_1 else game.fta_away for game in games_stats)
        total_ftm_team_1 = sum(game.ftm_home if game.team_id_home == team_id_1 else game.ftm_away for game in games_stats)
        # További aggregációs műveletek...

        total_pts_team_2 = sum(game.pts_home if game.team_id_home == team_id_2 else game.pts_away for game in games_stats)
        total_ast_team_2 = sum(game.ast_home if game.team_id_home == team_id_2 else game.ast_away for game in games_stats)
        total_reb_team_2 = sum(game.reb_home if game.team_id_home == team_id_2 else game.reb_away for game in games_stats)
        total_dreb_team_2 = sum(game.dreb_home if game.team_id_home == team_id_2 else game.dreb_away for game in games_stats)
        total_oreb_team_2 = sum(game.oreb_home if game.team_id_home == team_id_2 else game.oreb_away for game in games_stats)
        total_stl_team_2 = sum(game.stl_home if game.team_id_home == team_id_2 else game.stl_away for game in games_stats)
        total_blk_team_2 = sum(game.blk_home if game.team_id_home == team_id_2 else game.blk_away for game in games_stats)
        total_tov_team_2 = sum(game.tov_home if game.team_id_home == team_id_2 else game.tov_away for game in games_stats)
        total_pf_team_2 = sum(game.pf_home if game.team_id_home == team_id_2 else game.pf_away for game in games_stats)
        total_fga_team_2 = sum(game.fga_home if game.team_id_home == team_id_2 else game.fga_away for game in games_stats)
        total_fgm_team_2 = sum(game.fgm_home if game.team_id_home == team_id_2 else game.fgm_away for game in games_stats)
        total_fg3a_team_2 = sum(game.fg3a_home if game.team_id_home == team_id_2 else game.fg3a_away for game in games_stats)
        total_fg3m_team_2 = sum(game.fg3m_home if game.team_id_home == team_id_2 else game.fg3m_away for game in games_stats)
        total_fta_team_2 = sum(game.fta_home if game.team_id_home == team_id_2 else game.fta_away for game in games_stats)
        total_ftm_team_2 = sum(game.ftm_home if game.team_id_home == team_id_2 else game.ftm_away for game in games_stats)
        # További aggregációs műveletek...

        # Az eredmények átalakítása JSON formátumba
        result = {
            "team_1": {
                "team_id": team_id_1,
                "total_pts": round(total_pts_team_1),
                "total_ast": round(total_ast_team_1),
                "total_reb": round(total_reb_team_1),
                "total_dreb": round(total_dreb_team_1),
                "total_oreb": round(total_oreb_team_1),
                "total_stl": round(total_stl_team_1),
                "total_blk": round(total_blk_team_1),
                "total_tov": round(total_tov_team_1),
                "total_pf": round(total_pf_team_1),
                "total_fga": round(total_fga_team_1),
                "total_fgm": round(total_fgm_team_1),
                "total_fg3a": round(total_fg3a_team_1),
                "total_fg3m": round(total_fg3m_team_1),
                "total_fta": round(total_fta_team_1),
                "total_ftm": round(total_ftm_team_1),
            
                "avg_fg_pct_team_1": round(mean(safely_convert_to_float(game.fg_pct_home) if game.team_id_home == team_id_1 else safely_convert_to_float(game.fg_pct_away) for game in games_stats)*100),
                "avg_fg3_pct_team_1": round(mean(safely_convert_to_float(game.fg3_pct_home) if game.team_id_home == team_id_1 else safely_convert_to_float(game.fg3_pct_away) for game in games_stats)*100),
                "avg_ft_pct_team_1": round(mean(safely_convert_to_float(game.ft_pct_home) if game.team_id_home == team_id_1 else safely_convert_to_float(game.ft_pct_away) for game in games_stats)*100),
                # További aggregált adatok...
            },
            "team_2": {
                "team_id": team_id_2,
                "total_pts": round(total_pts_team_2),
                "total_ast": round(total_ast_team_2),
                "total_reb": round(total_reb_team_2),
                "total_dreb": round(total_dreb_team_2),
                "total_oreb": round(total_oreb_team_2),
                "total_stl": round(total_stl_team_2),
                "total_blk": round(total_blk_team_2),
                "total_tov": round(total_tov_team_2),
                "total_pf": round(total_pf_team_2),
                "total_fga": round(total_fga_team_2),
                "total_fgm": round(total_fgm_team_2),
                "total_fg3a": round(total_fg3a_team_2),
                "total_fg3m": round(total_fg3m_team_2),
                "total_fta": round(total_fta_team_2),
                "total_ftm": round(total_ftm_team_2),
            
                "avg_fg_pct_team_2":  round(mean(safely_convert_to_float(game.fg_pct_home) if game.team_id_home == team_id_2 else safely_convert_to_float(game.fg_pct_away) for game in games_stats)*100),
                "avg_fg3_pct_team_2": round(mean(safely_convert_to_float(game.fg3_pct_home) if game.team_id_home == team_id_2 else safely_convert_to_float(game.fg3_pct_away) for game in games_stats)*100),
                "avg_ft_pct_team_2": round(mean(safely_convert_to_float(game.ft_pct_home) if game.team_id_home == team_id_2 else safely_convert_to_float(game.ft_pct_away) for game in games_stats)*100),
                # További aggregált adatok...
            },
        }

        return jsonify(result)