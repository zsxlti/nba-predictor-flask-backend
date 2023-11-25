import re
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/api/register")
class UserRegister(MethodView):
      def post(self):
            user_data = request.get_json()

            # Jelszó ellenőrzése reguláris kifejezéssel
            password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')

            if not password_pattern.match(user_data["password"]):
                  return {"error": "Invalid password! Password must be at least 8 characters long and include uppercase, lowercase, and a number."}, 400

            # Ha az ellenőrzés sikeres, felhasználó létrehozása
            user = UserModel(
                  username=user_data["username"],
                  password=pbkdf2_sha256.hash(user_data["password"])
            )
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully."}, 201
        
@blp.route("/api/login")
class UserLogin(MethodView):
      @blp.arguments(UserSchema)
      def post(self, user_data):
            user = UserModel.query.filter(
                  UserModel.username == user_data["username"]
            ).first()

            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                  access_token = create_access_token(identity=user.id, fresh=True)
                  refresh_token = create_refresh_token(identity=user.id)
                  return {"access_token": access_token, "refresh_token": refresh_token}
            
            abort(401, message="Invalid credentials.")

@blp.route("/api/refresh")
class TokenRefresh(MethodView):
      @jwt_required(refresh=True)
      def post(self):
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"access_token": new_token}

@blp.route("/api/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
          jti = get_jwt()["jti"]
          BLOCKLIST.add(jti)
          return {"message": "Successfully logged out."}

@blp.route("/api/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            return user
    
    def delete(self, user_id):
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted."}, 200

@blp.route("/api/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()