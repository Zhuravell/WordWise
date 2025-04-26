#SQLAlchemy table definitions

#Define your database schema using SQLAlchemy (e.g. the DutchVocab model).
#Also, set up your engine and session (or import them in crud.py).

#Bot Username: WordWiseDbot

from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# DutchEnglishVocab is the Python class (ORM model) that represents your PostgreSQL table. Python uses this name
# __tablename__ = "dutch_english_vocab" links this class to the actual table name in the database. SQL uses this name. 
class DutchEnglishVocab(Base):
    __tablename__ = "dutch_english_vocab" #__tablename__ - special variable(a keyword in SQLAlchemy) a must for declarative base models
    
    id_word = Column(Integer, primary_key=True ,autoincrement=True)
    dutch_word = Column(Text, nullable=False)
    english_word = Column(Text, nullable = False)
    example_sentence = Column(Text, nullable = False)
    comment = Column(Text, nullable = True)
    source = Column(Text, nullable = True)
    added_at = Column (TIMESTAMP, server_default=func.now())
    
    
    
    