import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_required

from mybiomarker.app import serve_dash_app

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def protect_dashviews(dashapp):
    """If you want your Dash app to require a login,
    call this function with the Dash app you want to protect"""

    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func]
            )


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from mybiomarker.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user.
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from mybiomarker.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from mybiomarker.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from mybiomarker import models

    with app.app_context():
        db.create_all()

    dash_app = serve_dash_app(app)

    dash_app.run_server()

    protect_dashviews(dash_app)
    return app
