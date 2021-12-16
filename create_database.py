import sqlalchemy as db
import json
import os

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
 
class Database:
    def __init__(self, connection_url) -> None:
        self.connection_url= connection_url 
        self.engine = db.create_engine(self.connection_url)
        self.metadata = db.MetaData()
        self.game = None
        ## it should be in this format dialect+driver://username:password@host:port/database

    def create_DB_tables(self):
         
        self.metadata.clear()
        self.game = db.Table('game', self.metadata,
                      db.Column('id', db.Integer(), primary_key=True),
                      db.Column('steam_appid', db.Integer()),
                      db.Column('name', db.String(255), nullable=False),
                      db.Column('type', db.String(50)),
                      db.Column('required_age', db.Integer()),
                      db.Column('is_free', db.Boolean()),
                      # db.Column('detailed_description', db.String(1000)),
                      # db.Column('about_the_game', db.String(1000)),
                      db.Column('short_description', db.String(500)),
                      db.Column('supported_languages', db.String(255)),
                      db.Column('header_image', db.String(255)),
                      db.Column('website', db.String(50)),
                      db.Column('developers', db.String(100)),
                      db.Column('publishers', db.String(100))
                      )

        self.metadata.create_all(self.engine) #Creates the table


    def insert_data_to_table(self):

        # Opening JSON file
        f = open('data/database.json')
        
        data = json.load(f)
        connection = self.engine.connect()
        value_list =[]
        for i in data:
            
            value_list.append({
              'id' : i,
              'steam_appid':data[i]['steam_appid'],
              'name':data[i]['name'],
              'type':data[i]['type'],
              'required_age':data[i]['required_age'],
              'is_free':data[i]['is_free'],
              # 'detailed_description':data[i]['detailed_description'],
              # 'about_the_game':data[i]['about_the_game'],
              'short_description':data[i]['short_description'],
              'supported_languages':data[i]['supported_languages'],
              'header_image':data[i]['header_image'],
              'website':data[i]['website'],
              'developers': ', '.join(data[i]['developers']) if 'developers' in data[i] else None,
              'publishers': ', '.join(data[i]['publishers']) if 'publishers' in data[i] else None
            })
        query = db.insert(self.game)
        ResultProxy = connection.execute(query, value_list)
        
        f.close()

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "data/gamedatabase.db"))

database = Database(database_file)
database.create_DB_tables()
database.insert_data_to_table()