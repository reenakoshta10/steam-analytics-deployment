import sqlalchemy as db
import json
import os

from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.sql.sqltypes import Date

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
    legal_notice = Column(String)
    developers = Column(String)
    publishers = Column(String)
    currency = Column(String)
    price_initial = Column(Integer)
    price_final = Column(Integer)
    discount_on_price = Column(Integer)
    price_USD = Column(Integer)
    packages = Column(String)
    windows = Column(Boolean)
    mac = Column(Boolean)
    linux = Column(Boolean)
    categories = Column(String)
    genres = Column(String)
    coming_soon = Column(Boolean)
    release_date = Column(String)
    num_reviews = Column(Integer)
    review_score = Column(Integer)
    total_positive = Column(Integer)
    total_negative = Column(Integer)
    total_reviews = Column(Integer)
    support_url = Column(String)
    support_email = Column(String)
class system_requirements(Base):
    __tablename__ = "system_requirements"

    id = Column(Integer, primary_key=True)
    minimum = Column(String)
    recommended = Column(String)
    system_type = Column(String)
    steam_appid = Column(Integer, ForeignKey(Game.id))
    
class package_groups(Base):
  __tablename__ = "package_groups"

  id = Column(Integer, primary_key=True)
  name = Column(String)
  title = Column(String)
  description = Column(String)
  is_recurring_subscription = Column(String)
  sub_package = Column(String)
  
class sub_package(Base):
  __tablename__ = "sub_package"

  package_id = Column(Integer, primary_key=True)
  is_free_license = Column(Boolean)
  price_in_cents_with_discount = Column(Integer)
  