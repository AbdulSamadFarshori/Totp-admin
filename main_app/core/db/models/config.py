from main_app import db, marshmallow
from main_app.core.db.models.base import Base


class Config(Base):
   access_token = db.Column(db.String(255))

class ConfigSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Config
        include_fk = True