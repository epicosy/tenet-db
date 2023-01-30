import contextlib
from typing import Union, Dict, Callable, Any, List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from tenetdb.exc import TenetDBError
from tenetdb.tables import *


class Database:
    def __init__(self, dialect: str, username: str, password: str, host: str, port: int, database: str,
                 debug: bool = False):

        self.url = f"{dialect}://{username}:{password}@{host}:{port}/{database}"

        if not database_exists(self.url):
            try:
                create_database(url=self.url, encoding='utf8')
            except TypeError as te:
                raise TenetDBError(f"Could not create database @{host}:{port}/{database}. {te}")

        self.engine = create_engine(self.url, echo=debug)
        Base.metadata.create_all(bind=self.engine)

    def refresh(self, entity: Base):
        with Session(self.engine) as session, session.begin():
            session.refresh(entity)

        return entity

    def add(self, entity: Base):
        with Session(self.engine) as session, session.begin():
            session.add(entity)
            session.flush()
            session.refresh(entity)
            session.expunge_all()

            if hasattr(entity, 'id'):
                return entity.id

    def add_all(self, entities: List[Base]) -> List[int]:
        with Session(self.engine) as session, session.begin():
            session.add_all(entities)

            return [e.id for e in entities if hasattr(e, 'id')]

    def destroy(self):
        # metadata = MetaData(self.engine, reflect=True)
        with contextlib.closing(self.engine.connect()) as con:
            trans = con.begin()
            Base.metadata.drop_all(bind=self.engine)
            trans.commit()

    def delete(self, entity: Base, entity_id: Union[int, str]):
        with Session(self.engine) as session, session.begin():
            return session.query(entity).filter(entity.id == entity_id).delete(synchronize_session='evaluate')

    def has_table(self, name: str):
        return self.engine.dialect.has_table(connection=self.engine.connect(), table_name=name)

    def filter(self, entity: Base, filters: Dict[Any, Callable], distinct: Any = None):
        with Session(self.engine) as session, session.begin():
            query = session.query(entity)

            for attr, exp in filters.items():
                query = query.filter(exp(attr))
            if distinct:
                query = query.distinct(distinct)
            session.expunge_all()
            return query

    def query(self, entity: Base, entity_id: Union[int, str] = None):
        with Session(self.engine) as session, session.begin():
            if entity_id and hasattr(entity, 'id'):
                results = session.query(entity).filter(entity.id == entity_id).first()
            else:
                results = session.query(entity).all()

            session.expunge_all()
            return results

    def query_attr(self, entity: Base, entity_id: int, attr: str):
        with Session(self.engine) as session, session.begin():
            if hasattr(entity, 'id') and hasattr(entity, attr):
                results = session.query(entity).filter(entity.id == entity_id).first()
                attr_result = getattr(results, attr)
                session.expunge_all()
                return attr_result

    def update(self, entity: Base, entity_id: int, attr: str, value):
        with Session(self.engine) as session, session.begin():
            if hasattr(entity, 'id') and hasattr(entity, attr):
                session.query(entity).filter(entity.id == entity_id).update({attr: value})
            else:
                raise TenetDBError(f"Could not update {type(entity)} {attr} with value {value}")

