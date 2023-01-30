import pandas as pd

from tenetdb.db import Database
from tenetdb.tables import Tag, Operation, Phase, Class, Abstraction, CWE, CWEOperation, CWEPhase, CWEClass


def populate_tags(database: Database):
    if not database.query(Tag):
        tags_df = pd.read_csv('tables/tags.csv')
        database.add_all([Tag(**row.to_dict()) for i, row in tags_df.iterrows()])


def populate_operations(database: Database):
    if not database.query(Operation):
        operations_df = pd.read_csv('tables/operations.csv')
        database.add_all([Operation(**row.to_dict()) for i, row in operations_df.iterrows()])


def populate_phases(database: Database):
    if not database.query(Phase):
        phases_df = pd.read_csv('tables/phases.csv')
        database.add_all([Phase(**row.to_dict()) for i, row in phases_df.iterrows()])


def populate_classes(database: Database):
    if not database.query(Class):
        classes_df = pd.read_csv('tables/classes.csv')
        database.add_all([Class(**row.to_dict()) for i, row in classes_df.iterrows()])


def populate_abstractions(database: Database):
    if not database.query(Abstraction):
        abstractions_df = pd.read_csv('tables/abstractions.csv')
        database.add_all([Abstraction(**row.to_dict()) for i, row in abstractions_df.iterrows()])


def populate_cwes(database: Database):
    if not database.query(CWE):
        cwes_df = pd.read_csv('tables/cwes.csv')
        database.add_all([CWE(**row.to_dict()) for i, row in cwes_df.iterrows()])


def populate_relationships(database: Database):
    if not database.query(CWEOperation):
        cwe_operation_df = pd.read_csv('tables/cwe_operation.csv')
        database.add_all([CWEOperation(**row.to_dict()) for i, row in cwe_operation_df.iterrows()])

    if not database.query(CWEPhase):
        cwe_phase_df = pd.read_csv('tables/cwe_phase.csv')
        database.add_all([CWEPhase(**row.to_dict()) for i, row in cwe_phase_df.iterrows()])

    if not database.query(CWEClass):
        cwe_class_df = pd.read_csv('tables/cwe_class.csv')
        database.add_all([CWEClass(**row.to_dict()) for i, row in cwe_class_df.iterrows()])


def populate_all(database: Database):
    populate_abstractions(database)
    populate_tags(database)
    populate_operations(database)
    populate_phases(database)
    populate_classes(database)
    populate_cwes(database)
    populate_relationships(database)
