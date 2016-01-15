from flask import Flask

App = Flask(__name__)

App.secret_key = 'add_later'

App.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/apeksha'

from models import db
db.init_app(App)

import app.routes
