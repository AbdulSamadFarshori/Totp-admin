import logging
import pytz
from datetime import datetime
from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from main_app import db
from main_app.core.authentication import authanticate
from main_app.core.db.models.client_model import ClientData
from main_app.core.db.models.config import Config
from main_app.core.decorators import login_required
from main_app.core.db.models.finger_print import FingerPrintData
from main_app.core.totp import create_google_auth_uri


totp_route = Blueprint('totp_route', __name__)

@totp_route.route('/home')
@login_required
def index():
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    data = ClientData.query.all()

    return render_template('home.html', data=data, access_token=access_token)

@totp_route.route('/home/get-totp/<pk>')
@login_required
def get_totp(pk):
    fp = FingerPrintData(client_id=pk, api_updated_at=datetime.now(tz=pytz.timezone('Asia/Kolkata')))
    db.session.add(fp)
    db.session.commit()
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    return render_template('get-totp.html', client_id=pk, access_token=access_token)

@totp_route.route('/home/update/<pk>')
@login_required
def update_totp(pk):
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token
    data = ClientData.query.filter_by(id=pk).first()
    return render_template('update-totp.html', id=pk, data=data, access_token=access_token)

@totp_route.route('/home/add')
@login_required
def add_totp():
    access_token_obj = Config.query.filter_by(id=1).first()
    access_token = access_token_obj.access_token         
    return render_template('add-totp.html', access_token=access_token)

@totp_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']
        auth = authanticate(email, password)
        print(auth)
        if auth:
            session['logged'] = True
            return redirect(url_for('totp_route.index'))
    return render_template('login.html')

@totp_route.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('totp_route.index'))


