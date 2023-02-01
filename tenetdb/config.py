from os import environ

_uname = environ['DB_USERNAME']
_pwd = environ['DB_PASSWORD']
_host = environ["DB_HOST"]
_port = environ["DB_PORT"]
_db_name = environ["DB_DATABASE"]


class Config(object):
    ENV = environ["ENV"] if "ENV" in environ else "DEVELOPMENT"
    CSRF_ENABLED = True
    SECRET_KEY = "SECRET_KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{_uname}:{_pwd}@{_host}:{_port}/{_db_name}"
