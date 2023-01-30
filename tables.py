from sqlalchemy import Column, Integer, Double, DateTime, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Operation(Base):
    __tablename__ = "operation"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    cwes = relationship('CWE', secondary="cwe_operation", backref='operations')


class Phase(Base):
    __tablename__ = "phase"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    acronym = Column('acronym', String, nullable=False)
    url = Column('url', String, nullable=True)
    cwes = relationship('CWE', secondary="cwe_phase", backref='phases')


class Class(Base):
    __tablename__ = "class"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    url = Column('url', String, nullable=True)
    cwes = relationship('CWE', secondary="cwe_class", backref='classes')


class Abstraction(Base):
    __tablename__ = "abstraction"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    cwes = relationship('CWE', backref='abstraction')


class CWE(Base):
    __tablename__ = "cwe"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    url = Column('url', String, nullable=False)
    abstraction_id = Column(Integer, ForeignKey('abstraction.id'))
    vulnerabilities = relationship('Vulnerability', secondary="vulnerability_cwe", backref='cwes')


class CWEOperation(Base):
    __tablename__ = "cwe_operation"
    __table_args__ = (
        PrimaryKeyConstraint('cwe_id', 'operation_id'),
    )

    cwe_id = Column('cwe_id', Integer, ForeignKey('cwe.id'))
    operation_id = Column('operation_id', Integer, ForeignKey('operation.id'))


class CWEPhase(Base):
    __tablename__ = "cwe_phase"
    __table_args__ = (
        PrimaryKeyConstraint('cwe_id', 'phase_id'),
    )

    cwe_id = Column('cwe_id', Integer, ForeignKey('cwe.id'))
    phase_id = Column('phase_id', Integer, ForeignKey('phase.id'))


class CWEClass(Base):
    __tablename__ = "cwe_class"
    __table_args__ = (
        PrimaryKeyConstraint('cwe_id', 'class_id'),
    )

    cwe_id = Column('cwe_id', Integer, ForeignKey('cwe.id'))
    class_id = Column('class_id', Integer, ForeignKey('class.id'))


class Tag(Base):
    __tablename__ = "tag"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    references = relationship("Reference", secondary="reference_tag", backref='tags')


class Reference(Base):
    __tablename__ = "reference"

    id = Column('id', Integer, primary_key=True)
    url = Column('url', String, nullable=False)
    vulnerability_id = Column(String, ForeignKey('vulnerability.id'))


class ReferenceTag(Base):
    __tablename__ = 'reference_tag'
    __table_args__ = (
        PrimaryKeyConstraint('reference_id', 'tag_id'),
    )

    reference_id = Column('reference_id', Integer, ForeignKey('reference.id'))
    tag_id = Column('tag_id', Integer, ForeignKey('tag.id'))


class Vulnerability(Base):
    __tablename__ = "vulnerability"

    id = Column('id', String, primary_key=True)
    description = Column('description', String, nullable=True)
    severity = Column('severity', Double, nullable=True)
    exploitability = Column('exploitability', Double, nullable=True)
    impact = Column('impact', Double, nullable=True)
    published_date = Column('published_date', DateTime, nullable=False)
    last_modified_date = Column('last_modified_date', DateTime, nullable=False)
    references = relationship("Reference", backref="vulnerability")


class VulnerabilityCWE(Base):
    __tablename__ = 'vulnerability_cwe'
    __table_args__ = (
        PrimaryKeyConstraint('vulnerability_id', 'cwe_id'),
    )

    vulnerability_id = Column('vulnerability_id', String, ForeignKey('vulnerability.id'))
    cwe_id = Column('cwe_id', Integer, ForeignKey('cwe.id'))
