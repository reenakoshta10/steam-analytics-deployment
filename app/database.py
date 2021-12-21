import sqlalchemy as db
import json
import os

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()

# an example mapping using the base
class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    steam_appid = Column(Integer)
    name = Column(String, nullable=False)
    type = Column(String)
    required_age = Column(Integer)
    is_free = Column(Boolean)
    short_description = Column(String)
    supported_languages = Column(String)
    header_image = Column(String)
    website = Column(String)
    developers = Column(String)
    publishers = Column(String)
    price = Column(Integer)