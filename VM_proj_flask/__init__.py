from flask import Flask

from config import Config
from VM_proj_flask.extensions import db, bycript, mail, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    bycript.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # Register blueprints here
    from VM_proj_flask.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

def create_db(app):
    with app.app_context():
        db.create_all()
        db.session.commit()
    print("Created Database!")

