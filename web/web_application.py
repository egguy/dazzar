import logging
import re

from flask import Flask, abort, jsonify, request, render_template, url_for, session, json, g, redirect, abort
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_openid import OpenID

from common.models import db, User
from common.configuration import load_config
from common.helpers import validate_nickname

app = Flask(__name__)
load_config(app)
db.init_app(app)
migrate = Migrate(app, db)

# Login Setup


oid = OpenID(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ladder/play')
@login_required
def ladder_play():
    return render_template('ladder_play.html')


@app.route('/ladder/scoreboard')
def ladder_scoreboard():
    return render_template('ladder_scoreboard.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/steam')
@oid.loginhandler
def login_steam():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return oid.try_login('http://steamcommunity.com/openid')


_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')


@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    user = User.get_or_create(match.group(1))
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.before_request
def nickname_checker():
    if request.endpoint == 'nickname' or request.endpoint == 'logout':
        return None

    if current_user.is_authenticated and (current_user.nickname is None):
        return redirect(url_for('nickname'))
    return None


@app.route('/nickname', methods=['GET', 'POST'])
def nickname():
    if (not current_user.is_authenticated) or (current_user.nickname is not None):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('nickname.html')
    elif request.method == 'POST':
        posted_nickname = request.form.get('nickname')
        if validate_nickname(posted_nickname) is None:
            session = db.session()
            user = session.query(User).filter_by(id=current_user.id).first()
            user.nickname = posted_nickname
            db.session().commit()
        return redirect(url_for('index'))

    abort(404)


if __name__ == "__main__":
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8000)
    IOLoop.instance().start()