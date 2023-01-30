import argparse

from os import environ

from tenetdb.db import Database
from tenetdb.populate import populate_all

_username = environ.get('POSTGRES_USER')
_password = environ.get('POSTGRES_PASSWORD')
_database = environ.get('POSTGRES_DB')


def main(dialect: str = 'postgresql', username: str = _username, password: str = _password, host: str = 'localhost',
         port: int = 5432, database: str = _database, debug: bool = True):
    db = Database(dialect=dialect, username=username, password=password, host=host, port=port, database=database,
                  debug=debug)

    print(f"Connected to {dialect}://{username}@{host}:{port}/{database}")
    populate_all(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI')
    parser.add_argument('--dialect', type=str, metavar='dialect', help='dialect', default='postgresql')
    parser.add_argument('--username', type=str, metavar='username', help='username', default='tenet')
    parser.add_argument('--password', type=str, metavar='password', help='password', default='tenet123')
    parser.add_argument('--host', type=str, metavar='host', help='host', default='localhost')
    parser.add_argument('--database', type=str, metavar='database', help='database', default='tenet')
    parser.add_argument('--debug', action='store_true', help='debug')
    parser.add_argument('--port', type=int, metavar='port', help='port', default=5432)
    args = parser.parse_args()

    main(dialect=args.dialect, username=args.username, password=args.password, host=args.host, port=args.port,
         database=args.database, debug=args.debug)
