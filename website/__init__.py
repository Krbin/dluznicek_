from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SzoZXA4sDQvFTZCA59YEcWLLq0kJmGmV"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Group, Payment, Debt

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        if not Group.query.filter_by(name="test").first():
            new_group = Group(name="test")
            db.session.add(new_group)
            db.session.commit()

    @login_manager.user_loader
    def load_user(id):
        return Group.query.get(int(id))

    return app
