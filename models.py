from datetime import datetime

from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DeclarativeBase = declarative_base()

import config

class Citation(DeclarativeBase):
    __tablename__ = 'bibbot'

    id = Column(Integer, primary_key=True)
    domain = Column('domain', String)
    channel = Column('channel', String)
    user = Column('user', String)
    text = Column('text', String)
    bibtex = Column('bibtex', String)
    url = Column('url', String)
    time = Column('time', DateTime)


engine = create_engine(URL(**config.DATABASE))
DeclarativeBase.metadata.create_all(engine)

def add_citation(item):
    session = sessionmaker(bind=engine)()
    citation = Citation(**item)
    try:
        session.add(citation)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
