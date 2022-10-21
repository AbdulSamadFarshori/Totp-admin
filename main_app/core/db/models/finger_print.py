from main_app import db, marshmallow
from main_app.core.db.models.base import Base


class FingerPrintData(Base):
   client_id = db.Column(db.String(255))

class FingerPrintDataSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = FingerPrintData
        include_fk = True