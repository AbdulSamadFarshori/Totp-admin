from datetime import datetime
from http import client

from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, reqparse

from main_app import db
from main_app.core.db.models.client_model import ClientData, ClientDataSchema
from main_app.core.decorators import limiter
from main_app.core.totp import get_current_totp, create_google_auth_uri

nsApi = Namespace('client', description=' operations')

@nsApi.route('/fetch-data')
class GetClientDataList(Resource):
    @nsApi.doc('fetch list from database')
    @jwt_required()
    def get(self):
        schema = ClientDataSchema(many=True)
        data = ClientData.query.all()
        return schema.dump(data)
    
@nsApi.route('/get-data/<pk>')
class GetClientData(Resource):
    @nsApi.doc('fetch list from database')
    @jwt_required()
    def get(self, pk):
        schema = ClientDataSchema()
        data = ClientData.query.filter_by(id=pk).first()
        return schema.dump(data)

@nsApi.route('/current-totp/<clientId>')
class GetCurrentTotp(Resource):
    @nsApi.doc('get current totp code')
    @jwt_required()
    def post(self, clientId):
        data = ClientData.query.filter_by(client_id=clientId).first()
        key = data.totp_key
        current_totp = get_current_totp(key)
        uri = create_google_auth_uri(key)
        return {'totp_code':current_totp, 'uri':uri}
    
@nsApi.route('/add-data')
class AddNewClientData(Resource):
    @limiter
    @nsApi.doc('add new data in database')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str)
        parser.add_argument('totp_key', type=str)
        args = parser.parse_args()
        result = ClientData(client_id=args.client_id, totp_key=args.totp_key)
        db.session.add(result)
        db.session.commit()
        return {"status":True, "msg":"data has uploaded successfully!"}
    
@nsApi.route('/update-data/<pk>')
class UpdateClientData(Resource):
    @nsApi.doc('update data in database')
    @jwt_required()
    def put(self, pk):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str)
        parser.add_argument('totp_key', type=str)
        args = parser.parse_args()
        result = ClientData.query.filter_by(client_id=pk).first()
        result.client_id = args.client_id
        result.totp_key = args.totp_key
        db.session.commit()
        return {"msg":"data has been updated successfully"}
    
@nsApi.route('/delete-data/<pk>')
class DeleteClientData(Resource):
    @nsApi.doc('delete data')
    @jwt_required()
    def delete(self, pk):
        result = ClientData.query.filter_by(id=pk).delete()
        db.session.commit()
        return {"msg":"data has been deleted successfully"}
    

@nsApi.route('/search-client')
class SearchClientData(Resource):
    @nsApi.doc('seach client data')
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item', type=str)
        args = parser.parse_args()
        search =  f'%{args.item}%'
        output = ClientData.query.filter(ClientData.client_id.like(search)).all()
        schema = ClientDataSchema(many=True)
        return schema.dump(output)