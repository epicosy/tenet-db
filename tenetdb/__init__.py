from flask import Flask
from flask_graphql import GraphQLView
from tenetdb.config import Config
from tenetdb.graphql.schema import schema

#"postgresql://gzwddnlz:bAodjvU9QfoatkJu7GmRL8jdakxSGVbJ@rogue.db.elephantsql.com/gzwddnlz"


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["DEBUG"] = False if Config.ENV == "TESTING" else True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from tenetdb.models import db, init_app
    init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/")
    def test():
        return "Test ok!"

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

    return app
