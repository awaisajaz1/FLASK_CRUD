from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from crud_ops.myConfigs import Configs
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



def create_app(config_class=Configs):
    app = Flask(__name__)
    app.config.from_object(Configs)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from crud_ops.users.routes import users
    from crud_ops.posts.routes import posts
    from crud_ops.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app

