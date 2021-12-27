import os
import pandas as pd

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask_navigation import Navigation


import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import func
from sqlalchemy.sql import text

import matplotlib.pyplot as plt

app = Flask(__name__)
nav = Navigation(app)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "../data/gamedatabase.db")
)

engine = sqlalchemy.create_engine(database_file)

nav.Bar('top', [
    nav.Item('Data', 'get_data'),
    nav.Item('Data Visuals', 'visual'),
])

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/data")
def get_data():
    

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    inspector = inspect(engine)

    # Get table information
    print(inspector.get_table_names())

    data = None
    with engine.connect() as connection:
        df = pd.read_sql("game", connection)
        sort_by = request.args.get('column') if request.args.get('column') is not None else "total_reviews"
        order = True if (request.args.get('order') is not None and request.args.get('order') == 'True') else False
        print(type(order))
        print(sort_by, order)
        df['year_of_release'] = df["release_date"].apply(lambda d: int(d[-4:]))  
        df['unit_sold'] = df.apply(lambda x: calculate_unit_sold(x.total_reviews, x.year_of_release), axis= 1)
        df['revenue'] = df['unit_sold']* df["price_USD"]
        columns = ["name",	"required_age",	"is_free",	"price_USD",	"windows",	"mac", "linux",	"categories",	"genres",	
        "coming_soon",	"release_date",	"total_positive",	"total_negative",	"total_reviews","year_of_release","unit_sold","revenue"]
        df['revenue']= df['revenue'].fillna(value=0)
        df['price_USD']= df['price_USD'].fillna(value=0)
        df = df.sort_values(by =[sort_by],ascending=order)
        print(df.shape)
        data = df.head(25)  
        data = data[columns]
    return render_template(
        "data.html", tables=[data.to_html(classes="data", index=False)], titles=data.columns.values, selected_column= "total_reviews", column_order= False)

@app.route("/")
@app.route("/visual")
def visual():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    with engine.connect() as connection:
        df = pd.read_sql("game", connection)
        columns = ["name",	"required_age",	"is_free",	"price_USD",	"windows",	"mac", "linux",	"categories",	"genres",	
        "coming_soon",	"release_date",	"total_positive",	"total_negative",	"total_reviews"]
        df = df[columns]
        df['year_of_release'] = df["release_date"].apply(lambda d: int(d[-4:]))  
        df['unit_sold'] = df.apply(lambda x: calculate_unit_sold(x.total_reviews, x.year_of_release), axis= 1)
        df['revenue'] = df['unit_sold']* df["price_USD"] / 1000000
        df = df.sort_values(by =["revenue"],ascending=False)
        df = df.head(10)
    plt.figure(figsize=(24, 12), dpi=80)  # create figure & 1 axis
    colors= ['#78C850','#F08030','#6890F0','#A8B820','#A8A878', '#A040A0', '#F8D030', '#E0C068',
    '#EE99AC',  '#C03028', '#F85888', '#B8A038','#705898', '#98D8D8',  '#7038F8']
    plt.barh(df.head(10)["name"],df.head(10)["revenue"], color= colors[:10])
    plt.title("Top 10 Games based on revenue")
    plt.xlabel("Revenue in Millions")
    plt.ylabel("Game")
    plt.savefig('app/static/images/age_plot.png')
    return render_template("datavisuals.html")
 
@app.route("/insights")
def get_plot():
  os_name = request.args.get('os')
  print("selected os is ",os_name)
  with engine.connect() as connection:
    query = "select count("+os_name+") , "+os_name+" from game group by "+os_name+";"
    df = pd.read_sql(query, connection)
    df[os_name].replace({1: os_name, 0: "other os"}, inplace=True)
    print(df.head(10))
  fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
  ax.pie(df.iloc[:,0],labels = df.iloc[:,1], autopct='%1.1f%%')
  plt.title(f"Percentage of games are released on {os_name} systems")
  plt.savefig('app/static/images/age_plot.png')
  plt.close(fig) 
  return render_template("datavisuals.html")

def calculate_unit_sold(number_review, year_of_release):
  review_multiplier = 0

  if(year_of_release < 2014):
    review_multiplier = 60
  if(year_of_release >= 2014 and year_of_release<= 2016):
    review_multiplier = 50
  if(year_of_release == 2017):
    review_multiplier = 40
  if(year_of_release >= 2018 and year_of_release<= 2019):
    review_multiplier = 35
  if(year_of_release >= 2020):
    review_multiplier = 30
  return number_review * review_multiplier

      
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = os.environ.get('PORT'), debug=True)
