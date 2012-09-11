from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Event(Base):
    __tablename__ = 'mf_calendar_event'
    id = Column(Integer, primary_key=True)
    function_id = Column(Integer)
    periodic = Column(Integer)

    def __init__(self, function_id, periodic):
        self.function_id = function_id
        self.periodic = periodic

    def __repr__(self):
        return "<Event('%s','%s')>" % (self.function_id, self.periodic)