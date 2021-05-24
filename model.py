# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json
# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html
DeclarativeBase = declarative_base()

class Audited(DeclarativeBase):
    __tablename__ = "audited"

    id = Column('id', Integer, primary_key=True)
    host = Column('host', String)
    date = Column('date', DateTime)
    
    def __init__(self, host, date):
        self.host = host
        self.date = date

# engine = create_engine('postgresql://test:password@localhost:5432/project13')
engine = create_engine('sqlite:///db.sqlite')
DeclarativeBase.metadata.create_all(engine)