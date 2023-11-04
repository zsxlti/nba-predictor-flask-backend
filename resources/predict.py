import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import PredictionSchema
from models import GameModel

blp = Blueprint("Predictions", "predictions", description="Operations on predictions")

@blp.route("/predict")
class PredictionOutcome(MethodView):
    @blp.arguments(PredictionSchema)
    def post(self, prediction_data):
        training_data = GameModel.query.all()[-10000:]

        home_team_data = GameModel.query.filter(
             GameModel.team_id_home == prediction_data["team_id_home"]
        ).all()[-1]

        away_team_data = GameModel.query.filter(
             GameModel.team_id_away == prediction_data["team_id_away"]
        ).all()[-1]

        test_data_x = pd.DataFrame({
        "pts_home": [home_team_data.pts_home],
        "pts_away": [away_team_data.pts_away],
        "reb_home": [home_team_data.reb_home],
        "reb_away": [away_team_data.reb_away],
        "ast_home": [home_team_data.ast_home],
        "ast_away": [away_team_data.ast_away],
        })

        accuracy_test_data = GameModel.query.all()[:150]
        accuracy_data_x = pd.DataFrame({
        "pts_home": [data.pts_home for data in accuracy_test_data],
        "pts_away": [data.pts_away for data in accuracy_test_data],
        "reb_home": [data.reb_home for data in accuracy_test_data],
        "reb_away": [data.reb_away for data in accuracy_test_data],
        "ast_home": [data.ast_home for data in accuracy_test_data],
        "ast_away": [data.ast_away for data in accuracy_test_data],
        })

        accuracy_test_y = pd.DataFrame({
        "home_win": [data.home_win for data in accuracy_test_data]
        })



        training_data_x = pd.DataFrame({
        "pts_home": [data.pts_home for data in training_data],
        "pts_away": [data.pts_away for data in training_data],
        "reb_home": [data.reb_home for data in training_data],
        "reb_away": [data.reb_away for data in training_data],
        "ast_home": [data.ast_home for data in training_data],
        "ast_away": [data.ast_away for data in training_data],
        })

        training_data_y = pd.DataFrame({
        "home_win": [data.home_win for data in training_data]
        })

        print(training_data_x)

        # rf_model = RandomForestClassifier(n_estimators=100)
        # rf_model.fit(training_data_x,training_data_y)
        rf_model = joblib.load("random_forest.joblib")
        prediction_result = rf_model.predict(test_data_x)
        print(prediction_result)

        # accuracy_result = rf_model.predict(accuracy_data_x)
        # print(metrics.accuracy_score(accuracy_test_y, accuracy_result))

        # save
        # joblib.dump(rf_model, "random_forest.joblib")

        # load
        # loaded_rf = joblib.load("random_forest.joblib")


        return {"message": "Success."}, 201
    
