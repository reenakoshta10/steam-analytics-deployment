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


class Database:
    def __init__(self, connection_url) -> None:
        self.connection_url = connection_url
        self.engine = db.create_engine(self.connection_url)
        self.metadata = db.MetaData()

    def create_DB_tables(self):

        Base.metadata.create_all(self.engine)

    def insert_data_to_table(self):

        # Opening JSON file
        f = open("data/database.json")

        data = json.load(f)
        connection = self.engine.connect()
        value_list = []
        for i in data:

            value_list.append(
                {
                    "id": i,
                    "steam_appid": data[i]["steam_appid"],
                    "name": data[i]["name"],
                    "type": data[i]["type"],
                    "required_age": data[i]["required_age"],
                    "is_free": data[i]["is_free"],
                    "short_description": data[i]["short_description"],
                    "supported_languages": data[i]["supported_languages"],
                    "header_image": data[i]["header_image"],
                    "website": data[i]["website"],
                    "developers": ", ".join(data[i]["developers"])
                    if "developers" in data[i]
                    else None,
                    "publishers": ", ".join(data[i]["publishers"])
                    if "publishers" in data[i]
                    else None,
                }
            )
        query = db.insert(Game)
        ResultProxy = connection.execute(query, value_list)

        f.close()


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "data/gamedatabase.db"))

database = Database(database_file)
database.create_DB_tables()
database.insert_data_to_table()
