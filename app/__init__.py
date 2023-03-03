from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from .site.routes import site
from .authentication.routes import auth
from models import db as root_db, login_manager, ma
from .api.routes import api
from helpers import JSONEncoder

app = Flask(__name__)
CORS(app, resources = {'/*':{'origins': 'http://localhost:3000'}})

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)