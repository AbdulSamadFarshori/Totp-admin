from functools import wraps

from flask import jsonify, redirect, session

from main_app.core.db.models.client_model import ClientData


def limiter(func):
    @wraps(func)
    def wapper(*args, **kargs):
        total_number = ClientData.query.all()
        if len(total_number) > 1000:
            output = jsonify({'status':False, 'msg':'sorry you have reached the limit, please contact to the admin!'})
            return output
        else:
            output = func(*args, **kargs)
            return output
    return wapper

def login_required(func):
    @wraps(func)
    def wapper(*args, **kargs):
        print(session)
        if session:
            output = func(*args, **kargs)
            return output
        else:
            return redirect('/login')
    return wapper



