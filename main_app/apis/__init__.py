from flask import Blueprint
from flask_restplus import Api

from main_app.apis.account.authentication import nsApi as nsaccount
from main_app.apis.totp.client_api import nsApi as nsclient

blueprint = Blueprint("api", __name__)
api = Api(blueprint,
        title='API',
        version="1.0",
        description="-",
        doc="/doc")

api.add_namespace(nsclient, path="/client")
api.add_namespace(nsaccount, path="/accounts")