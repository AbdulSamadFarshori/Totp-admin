from main_app import db, marshmallow
from main_app.core.db.models.base import Base


class ClientData(Base):
   client_id = db.Column(db.String(255))
   totp_key = db.Column(db.String(255))

class ClientDataSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientData
        include_fk = True 