from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_message = "Ezt a műveletet, csak bejelentkezett személyek tehetik meg!"
login_manager.login_message_category = "danger"
login_manager.login_view = "login"


from webshop import routes