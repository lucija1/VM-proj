
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager)
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

bycript = Bcrypt()
mail = Mail()
login_manager = LoginManager()



