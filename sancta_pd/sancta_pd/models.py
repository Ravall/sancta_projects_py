from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Event(Base):
	__tablename__ = 'mf_calendar_event'
	id = Column(Integer, primary_key=True)
	function_id = Column(Integer)
	periodic = Column(Integer)

	@staticmethod
	def get_all():
		return DBSession.query(Event).all()
