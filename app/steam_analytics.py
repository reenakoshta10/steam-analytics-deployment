from io import BytesIO
import os
import pandas as pd
from database import Game

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask_navigation import Navigation


import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import func

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

@app.route("/")
def index():
    return render_template("index.html")

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
        df = df.sort_values(by =["price"],ascending=False)
        data = df.head(25)
        data.drop(
            columns=["id","short_description", "supported_languages", "header_image"],
            axis=1,
            inplace=True,
        )
        age_group_count = df.groupby('required_age').size()
    # fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    # ax.bar(age_group_count.index, age_group_count.values)
    # plt.savefig('app/static/images/my_plot.png')
    # plt.close(fig)    # close the figure window
    
    return render_template(
        "data.html", tables=[data.to_html(classes="data", index=False)], titles=data.columns.values
    )

@app.route("/visual")
@app.route("/visual/<int:except_age>")
def visual(except_age=None):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    
    if(except_age == None):
        result = session.query(func.count(Game.required_age), Game.required_age).group_by(Game.required_age).all()
    else:
        result = session.query(func.count(Game.required_age), Game.required_age).group_by(Game.required_age).filter(Game.required_age != except_age)
    x=[]
    y=[]
    for _row in result:
      y.append(_row[0])
      x.append(_row[1])
    print(x)
    print(y)
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    ax.pie(y,labels = x, autopct='%1.1f%%')
    plt.title("Games available for required minimum")
    plt.savefig('app/static/images/age_plot.png')
    plt.close(fig) 
    return render_template("datavisuals.html")
 
# @app.route('/fig/')
# def fig():
#       # plt.plot([1,2,3,4], [1,2,3,4])
#       plt.pie(data_for_plt['is_free'])
#       img = BytesIO()
#       plt.savefig(img)
#       img.seek(0)
#       return send_file(img, mimetype='image/png')
      
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = os.environ.get('PORT'), debug=True)
