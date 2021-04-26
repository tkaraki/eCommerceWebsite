from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

moment = Moment(app)
bootstrap = Bootstrap(app)

from app import routes, models, errors

#app.config.from_object(TestConfig)
