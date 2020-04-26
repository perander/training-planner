from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# login
from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps


def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", *current_user.roles()))

            if role not in acceptable_roles:
                return login_manager.unauthorized()

            return func(*args, **kwargs)

        return decorated_view

    return wrapper if _func is None else wrapper(_func)


from application.category import models

from application.tasks import models

from application.auth import models

from application.stats import views

# login part 2
from application.auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    db.create_all()
except:
    print("creating db failed")
    pass

from application.category import views

from application.tasks import views

from application.auth import views

from application import views
