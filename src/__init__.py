from flask import Flask

# Routes
from .routes import AuthRoutes
from .routes import UserRoutes

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix='/api/')
    #app.register_blueprint(LanguageRoutes.main, url_prefix='/languages')
    app.register_blueprint(UserRoutes.main, url_prefix='/api/user')

    return app
