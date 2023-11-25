from flask.views import MethodView
from flask_smorest import Blueprint
from models import GameModel
from sqlalchemy import or_

blp = Blueprint("Stats", "stats", description="Operations on stats")

@blp.route("/api/stats/<int:season_id>/<int:team_id>/<string:stat_type>")
class Stats(MethodView):
    @blp.response(200)
    def get(self, season_id, team_id, stat_type):
        # Check if stat_type is one of the allowed values ("pts", "reb", "ast", "stl", "blk", "tov", "pf")
        allowed_stat_types = ["pts", "reb", "ast", "stl", "blk", "tov", "pf"]
        if stat_type not in allowed_stat_types:
            return {"error": "Invalid stat_type"}, 400

        # Use SQLAlchemy to filter games based on season_id and team_id
        games = GameModel.query.filter(
            GameModel.season_id == season_id,
            or_(GameModel.team_id_home == team_id, GameModel.team_id_away == team_id)
        ).all()

        # Collect the selected statistics for the games
        results = []
        for game in games:
            if stat_type == "pts":
                if game.team_id_home == team_id:
                    stat_value = game.pts_home
                elif game.team_id_away == team_id:
                    stat_value = game.pts_away
            elif stat_type == "reb":
                if game.team_id_home == team_id:
                    stat_value = game.reb_home
                elif game.team_id_away == team_id:
                    stat_value = game.reb_away
            elif stat_type == "ast":
                if game.team_id_home == team_id:
                    stat_value = game.ast_home
                elif game.team_id_away == team_id:
                    stat_value = game.ast_away
            elif stat_type == "stl":
                if game.team_id_home == team_id:
                    stat_value = game.stl_home
                elif game.team_id_away == team_id:
                    stat_value = game.stl_away
            elif stat_type == "blk":
                if game.team_id_home == team_id:
                    stat_value = game.blk_home
                elif game.team_id_away == team_id:
                    stat_value = game.blk_away  
            elif stat_type == "tov":
                if game.team_id_home == team_id:
                    stat_value = game.tov_home
                elif game.team_id_away == team_id:
                    stat_value = game.tov_away
            elif stat_type == "pf":
                if game.team_id_home == team_id:
                    stat_value = game.pf_home
                elif game.team_id_away == team_id:
                    stat_value = game.pf_away                  

            game_date = game.date  # Game date
            result = {
                "game_date": game_date.strftime("%Y-%m-%d"),
                "stat_value": stat_value
            }
            results.append(result)

        if not results:
            return {"error": "Invalid team_id or no games found"}, 400

        return results


@blp.route("/api/stats/<int:season_id>/<int:team_id1>/<int:team_id2>/<string:stat_type>")
class Stats2(MethodView):
    @blp.response(200)
    def get(self, season_id, team_id1, team_id2, stat_type):
        # Check if stat_type is one of the allowed values ("pts", "reb", "ast", "stl", "blk", "tov", "pf")
        allowed_stat_types = ["pts", "reb", "ast", "stl", "blk", "tov", "pf"]
        if stat_type not in allowed_stat_types:
            return {"error": "Invalid stat_type"}, 400

        # Use SQLAlchemy to filter games based on season_id and team_id1
        games_team1 = GameModel.query.filter(
            GameModel.season_id == season_id,
            or_(GameModel.team_id_home == team_id1, GameModel.team_id_away == team_id1)
        ).all()

        # Collect the selected statistics for the games of team_id1
        results_team1 = []
        for game in games_team1:
            if stat_type == "pts":
                if game.team_id_home == team_id1:
                    stat_value = game.pts_home
                elif game.team_id_away == team_id1:
                    stat_value = game.pts_away
            elif stat_type == "reb":
                if game.team_id_home == team_id1:
                    stat_value = game.reb_home
                elif game.team_id_away == team_id1:
                    stat_value = game.reb_away
            elif stat_type == "ast":
                if game.team_id_home == team_id1:
                    stat_value = game.ast_home
                elif game.team_id_away == team_id1:
                    stat_value = game.ast_away
            elif stat_type == "stl":
                if game.team_id_home == team_id1:
                    stat_value = game.stl_home
                elif game.team_id_away == team_id1:
                    stat_value = game.stl_away
            elif stat_type == "blk":
                if game.team_id_home == team_id1:
                    stat_value = game.blk_home
                elif game.team_id_away == team_id1:
                    stat_value = game.blk_away  
            elif stat_type == "tov":
                if game.team_id_home == team_id1:
                    stat_value = game.tov_home
                elif game.team_id_away == team_id1:
                    stat_value = game.tov_away
            elif stat_type == "pf":
                if game.team_id_home == team_id1:
                    stat_value = game.pf_home
                elif game.team_id_away == team_id1:
                    stat_value = game.pf_away                  

            game_date = game.date  # Game date
            result = {
                "game_date1": game_date.strftime("%Y-%m-%d"),
                "stat_value1": stat_value
            }
            results_team1.append(result)

        # Use SQLAlchemy to filter games based on season_id and team_id2
        games_team2 = GameModel.query.filter(
            GameModel.season_id == season_id,
            or_(GameModel.team_id_home == team_id2, GameModel.team_id_away == team_id2)
        ).all()

        # Collect the selected statistics for the games of team_id2
        results_team2 = []
        for game in games_team2:
            if stat_type == "pts":
                if game.team_id_home == team_id2:
                    stat_value = game.pts_home
                elif game.team_id_away == team_id2:
                    stat_value = game.pts_away
            elif stat_type == "reb":
                if game.team_id_home == team_id2:
                    stat_value = game.reb_home
                elif game.team_id_away == team_id2:
                    stat_value = game.reb_away
            elif stat_type == "ast":
                if game.team_id_home == team_id2:
                    stat_value = game.ast_home
                elif game.team_id_away == team_id2:
                    stat_value = game.ast_away
            elif stat_type == "stl":
                if game.team_id_home == team_id2:
                    stat_value = game.stl_home
                elif game.team_id_away == team_id2:
                    stat_value = game.stl_away
            elif stat_type == "blk":
                if game.team_id_home == team_id2:
                    stat_value = game.blk_home
                elif game.team_id_away == team_id2:
                    stat_value = game.blk_away  
            elif stat_type == "tov":
                if game.team_id_home == team_id2:
                    stat_value = game.tov_home
                elif game.team_id_away == team_id2:
                    stat_value = game.tov_away
            elif stat_type == "pf":
                if game.team_id_home == team_id2:
                    stat_value = game.pf_home
                elif game.team_id_away == team_id2:
                    stat_value = game.pf_away                  

            game_date = game.date  # Game date
            result = {
                "game_date2": game_date.strftime("%Y-%m-%d"),
                "stat_value2": stat_value
            }
            results_team2.append(result)

        return {"team1": results_team1, "team2": results_team2}
