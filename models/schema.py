# Defines your database structure (table models).

from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):  # Inheriting from DeclarativeBase. Same as Base = declarative_base()
    pass

class DutchEnglishVocab(Base):
    __tablename__ = "dutch_english_vocab"
    
    id_word = Column(Integer, primary_key=True, autoincrement=True)
    dutch_word = Column(Text, nullable=False)
    english_word = Column(Text, nullable=False)
    example_sentence = Column(Text)
    comment = Column(Text)
    source = Column(Text)
    added_at = Column(TIMESTAMP, server_default=func.now())