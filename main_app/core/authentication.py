from main_app.core.db.models.user import User


def authanticate(email, password):

    verify = User.query.filter_by(email=email).first()
    if verify:
        if verify.password == password:
            return True
        return False
    return False
