from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask_restplus import Namespace, Resource, reqparse

from main_app import db
from main_app.core.db.models.config import Config
from main_app.core.db.models.user import User, UserSchema

nsApi = Namespace('authentication', description='auth operations')

@nsApi.route('/get-access-token')
class GetAccessTokenApi(Resource):
    @nsApi.doc('login system')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        auths = User.query.filter_by(email=args.email, password=args.password).first()
        if auths:
            access_token = create_access_token(identity=args.email)
            data = Config.query.filter_by(id=1).first()
            data.access_token = access_token
            data.api_updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify(message='Login Successful', access_token=access_token)
        else:
            return jsonify('Bad email or Password'), 401

@nsApi.route('/register')
class RegisterApi(Resource):
    @nsApi.doc('register system')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        auths = User(email=args.email, password=args.password)
        db.session.add(auths)
        db.session.commit()
        return {"message":"register Successful"}
        