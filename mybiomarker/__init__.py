import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_required


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



