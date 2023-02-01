import pandas as pd
import click

from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists

from tenetdb.exc import TenetDBError

db = SQLAlchemy()
parent_path = Path(__file__).parent


class Operation(db.Model):
    __tablename__ = "operation"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    cwes = db.relationship('CWE', secondary="cwe_operation", backref='operations')

    @staticmethod
    def populate():
        operations_df = pd.read_csv(f'{parent_path}/tables/operations.csv')
        db.session.add_all([Operation(**row.to_dict()) for i, row in operations_df.iterrows()])
        db.session.commit()


class Phase(db.Model):
    __tablename__ = "phase"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    acronym = db.Column('acronym', db.String, nullable=False)
    url = db.Column('url', db.String, nullable=True)
    cwes = db.relationship('CWE', secondary="cwe_phase", backref='phases')

    @staticmethod
    def populate():
        phases_df = pd.read_csv(f'{parent_path}/tables/phases.csv')
        db.session.add_all([Phase(**row.to_dict()) for i, row in phases_df.iterrows()])
        db.session.commit()


class BFClass(db.Model):
    __tablename__ = "bf_class"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    url = db.Column('url', db.String, nullable=True)
    cwes = db.relationship('CWE', secondary="cwe_bf_class", backref='bf_classes')

    @staticmethod
    def populate():
        classes_df = pd.read_csv(f'{parent_path}/tables/bf_classes.csv')
        db.session.add_all([BFClass(**row.to_dict()) for i, row in classes_df.iterrows()])
        db.session.commit()


class Abstraction(db.Model):
    __tablename__ = "abstraction"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    cwes = db.relationship('CWE', backref='abstraction')

    @staticmethod
    def populate():
        abstractions_df = pd.read_csv(f'{parent_path}/tables/abstractions.csv')
        db.session.add_all([Abstraction(**row.to_dict()) for i, row in abstractions_df.iterrows()])
        db.session.commit()


class CWE(db.Model):
    __tablename__ = "cwe"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    url = db.Column('url', db.String, nullable=False)
    abstraction_id = db.Column(db.Integer, db.ForeignKey('abstraction.id'))
    vulnerabilities = db.relationship('Vulnerability', secondary="vulnerability_cwe", backref='cwes')

    @staticmethod
    def populate():
        cwes_df = pd.read_csv(f'{parent_path}/tables/cwes.csv')
        db.session.add_all([CWE(**row.to_dict()) for i, row in cwes_df.iterrows()])
        db.session.commit()

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'url': self.url, 'abstraction_id': self.abstraction_id}


class CWEOperation(db.Model):
    __tablename__ = "cwe_operation"
    __table_args__ = (
        db.PrimaryKeyConstraint('cwe_id', 'operation_id'),
    )

    cwe_id = db.Column('cwe_id', db.Integer, db.ForeignKey('cwe.id'))
    operation_id = db.Column('operation_id', db.Integer, db.ForeignKey('operation.id'))

    @staticmethod
    def populate():
        cwe_operation_df = pd.read_csv(f'{parent_path}/tables/cwe_operation.csv')
        db.session.add_all([CWEOperation(**row.to_dict()) for i, row in cwe_operation_df.iterrows()])
        db.session.commit()


class CWEPhase(db.Model):
    __tablename__ = "cwe_phase"
    __table_args__ = (
        db.PrimaryKeyConstraint('cwe_id', 'phase_id'),
    )

    cwe_id = db.Column('cwe_id', db.Integer, db.ForeignKey('cwe.id'))
    phase_id = db.Column('phase_id', db.Integer, db.ForeignKey('phase.id'))

    @staticmethod
    def populate():
        cwe_phase_df = pd.read_csv(f'{parent_path}/tables/cwe_phase.csv')
        db.session.add_all([CWEPhase(**row.to_dict()) for i, row in cwe_phase_df.iterrows()])
        db.session.commit()


class CWEBFClass(db.Model):
    __tablename__ = "cwe_bf_class"
    __table_args__ = (
        db.PrimaryKeyConstraint('cwe_id', 'bf_class_id'),
    )

    cwe_id = db.Column('cwe_id', db.Integer, db.ForeignKey('cwe.id'))
    bf_class_id = db.Column('bf_class_id', db.Integer, db.ForeignKey('bf_class.id'))

    @staticmethod
    def populate():
        cwe_class_df = pd.read_csv(f'{parent_path}/tables/cwe_class.csv')
        db.session.add_all([CWEBFClass(**row.to_dict()) for i, row in cwe_class_df.iterrows()])
        db.session.commit()


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String, nullable=False)
    references = db.relationship("Reference", secondary="reference_tag", backref='tags')

    @staticmethod
    def populate():
        tags_df = pd.read_csv(f'{parent_path}/tables/tags.csv')
        db.session.add_all([Tag(**row.to_dict()) for i, row in tags_df.iterrows()])
        db.session.commit()


class Reference(db.Model):
    __tablename__ = "reference"

    id = db.Column('id', db.Integer, primary_key=True)
    url = db.Column('url', db.String, nullable=False)
    vulnerability_id = db.Column(db.String, db.ForeignKey('vulnerability.id'))


class ReferenceTag(db.Model):
    __tablename__ = 'reference_tag'
    __table_args__ = (
        db.PrimaryKeyConstraint('reference_id', 'tag_id'),
    )

    reference_id = db.Column('reference_id', db.Integer, db.ForeignKey('reference.id'))
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))


class Vulnerability(db.Model):
    __tablename__ = "vulnerability"

    id = db.Column('id', db.String, primary_key=True)
    description = db.Column('description', db.String, nullable=True)
    severity = db.Column('severity', db.Double, nullable=True)
    exploitability = db.Column('exploitability', db.Double, nullable=True)
    impact = db.Column('impact', db.Double, nullable=True)
    published_date = db.Column('published_date', db.DateTime, nullable=False)
    last_modified_date = db.Column('last_modified_date', db.DateTime, nullable=False)
    references = db.relationship("Reference", backref="vulnerability")


class VulnerabilityCWE(db.Model):
    __tablename__ = 'vulnerability_cwe'
    __table_args__ = (
        db.PrimaryKeyConstraint('vulnerability_id', 'cwe_id'),
    )

    vulnerability_id = db.db.Column('vulnerability_id', db.String, db.ForeignKey('vulnerability.id'))
    cwe_id = db.db.Column('cwe_id', db.Integer, db.ForeignKey('cwe.id'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    click.echo('Initializing the database.')

    if not Abstraction.query.all():
        Abstraction.populate()
        click.echo("Populated 'abstractions' table.")

    if not Tag.query.all():
        Tag.populate()
        click.echo("Populated 'tags' table.")

    if not Operation.query.all():
        Operation.populate()
        click.echo("Populated 'operations' table.")

    if not Phase.query.all():
        Phase.populate()
        click.echo("Populated 'phases' table.")

    if not BFClass.query.all():
        BFClass.populate()
        click.echo("Populated 'bf_classes' table.")

    if not CWE.query.all():
        CWE.populate()
        click.echo("Populated 'cwes' table.")

    if not CWEOperation.query.all():
        CWEOperation.populate()

    if not CWEPhase.query.all():
        CWEPhase.populate()

    if not CWEBFClass.query.all():
        CWEBFClass.populate()


def init_app(app):
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    db.init_app(app)

    if not database_exists(uri):
        try:
            create_database(url=uri, encoding='utf8')
        except TypeError as te:
            raise TenetDBError(f"Could not create database {uri.split('@')}. {te}")

    with app.app_context():
        db.create_all()
        app.cli.add_command(init_db_command)
