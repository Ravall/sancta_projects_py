import datetime
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def now():
    return datetime.datetime.now()

class Text(Base):
    __tablename__ = 'mf_system_text'

    id = Column(types.Integer, primary_key=True)
    title = Column(types.String)
    annonce = Column(types.Text)
    content = Column(types.Text)

class Object(Base):
    __tablename__ = 'mf_system_object'

    id = Column(types.Integer, primary_key=True)
    status = Column(types.Enum('active', 'pause', 'deleted'),default='active')
    created = Column(types.TIMESTAMP(), default=now())
    updated = Column(types.TIMESTAMP(), default=now())
    created_class = Column(types.String)

    text = relationship("TextObjectAssociation")

class TextObjectAssociation(Base):
    __tablename__ = 'mf_system_object_text'

    system_object_id = Column(types.Integer, ForeignKey('mf_system_object.id'), primary_key=True)
    system_text_id = Column(types.Integer, ForeignKey('mf_system_text.id'), primary_key=True)
    status =  Column(types.Enum('active', 'draft'), default='active')

    text = relationship("Text")

class RelationType(Base):
    __tablename__ = 'mf_system_relation_type'

    id = Column(types.Integer, primary_key=True)
    relation_name = Column(types.String)

class Relation(Base):
    __tablename__ = 'mf_system_relation'

    id = Column(types.Integer, primary_key=True)
    object_id = Column(types.Integer, ForeignKey('mf_system_object.id'))
    parent_object_id = Column(types.Integer, ForeignKey('mf_system_object.id'))
    relation_id = Column(types.Integer, ForeignKey('mf_system_relation_type.id'))



class Event(Base):
    __tablename__ = 'mf_calendar_event'

    id = Column(types.Integer, primary_key=True)
    function_id = Column(types.Integer)
    object_id = Column(types.Integer, ForeignKey('mf_system_object.id'),primary_key=True)
    periodic = Column(types.Integer)

    icons = relationship(
        "FileObject",
       # secondary="Relation",
        primaryjoin="and_(Relation.object_id==Event.object_id,Relation.parent_object_id==FileObject.object_id,Relation.relation_id=='2')"
    )

    @staticmethod
    def get_all():
        print DBSession.bind
        return DBSession.query(Event).all()



class FileObject(Base):
    __tablename__ = 'mf_system_file'

    id = Column(types.Integer, primary_key=True)
    object_id = Column(types.Integer, ForeignKey('mf_system_object.id'),primary_key=True)
    file_name = Column(types.String)

    object = relationship("Object")

    


