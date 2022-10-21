from main_app import db, marshmallow
from main_app.core.db.models.base import Base


class User(Base):
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True