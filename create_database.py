import sqlalchemy as db
import json
import os
import requests
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

from app.database import *
class Database:
    def __init__(self, connection_url) -> None:
        self.connection_url = connection_url
        self.engine = db.create_engine(self.connection_url)
        self.metadata = db.MetaData()
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        data= requests.get(url).json()
        self.currencies = data['rates']

    def create_DB_tables(self):
        Base.metadata.drop_all(bind=self.engine)
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
                    "legal_notice":data[i]["legal_notice"] if "legal_notice" in data[i]
                    else None,
                    "developers": ", ".join(data[i]["developers"])
                    if "developers" in data[i]
                    else None,
                    "publishers": ", ".join(data[i]["publishers"])
                    if "publishers" in data[i]
                    else None,
                    "currency" : data[i]["price_overview"]["currency"] if "price_overview" in data[i]
                    else None,
                    "price_initial" : data[i]["price_overview"]["initial"] if "price_overview" in data[i]
                    else None,
                    "price_final" : data[i]["price_overview"]["final"] if "price_overview" in data[i]
                    else None,
                    "discount_on_price" : data[i]["price_overview"]["discount_percent"] if "price_overview" in data[i]
                    else None,
                    "price_USD" : self.calculate_price(data[i]["price_overview"]["final"], data[i]["price_overview"]["currency"]) if "price_overview" in data[i]
                    else None,
                    "packages" : ", ".join(str(data[i]["packages"])) if "packages" in data[i]
                    else None,
                    "windows" : data[i]["platforms"]["windows"],
                    "mac" : data[i]["platforms"]["mac"],
                    "linux" : data[i]["platforms"]["linux"],
                    "categories" : self.get_categories(data[i]["categories"]) if "categories" in data[i]
                    else None,
                    "genres" : self.get_genres(data[i]["genres"]) if "genres" in data[i]
                    else None,
                    "coming_soon" : data[i]["release_date"]["coming_soon"],
                    "release_date" : data[i]["release_date"]["date"],
                    "num_reviews" : data[i]["num_reviews"],
                    "review_score" : data[i]["review_score"],
                    "total_positive" : data[i]["total_positive"],
                    "total_negative" : data[i]["total_negative"],
                    "total_reviews" : data[i]["total_reviews"],
                    "support_url" : data[i]["support_info"]["url"],
                    "support_email" : data[i]["support_info"]["email"]
                }
            )
        query = db.insert(Game)
        ResultProxy = connection.execute(query, value_list)

        f.close()

    def calculate_price(self, price, currency):
        amount = round(price / self.currencies[currency], 2) 
        return amount

    def get_categories(self, categories):
        cat=[]
        for category in categories:
          cat.append(category['description'])
        return ", ".join(cat)

    def get_genres(self, genres):
        genre_list=[]
        for genre in genres:
          genre_list.append(genre['description'])
        return ", ".join(genre_list)



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "data/gamedatabase.db"))

database = Database(database_file)
database.create_DB_tables()
database.insert_data_to_table()
