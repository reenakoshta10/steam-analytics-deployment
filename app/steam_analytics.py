from io import BytesIO
import os
import pandas as pd

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

app = Flask(__name__)
data_for_plt =[]

@app.route("/")
def index():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(
        os.path.join(project_dir, "../data/gamedatabase.db")
    )

    engine = sqlalchemy.create_engine(database_file)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    inspector = inspect(engine)

    # Get table information
    print(inspector.get_table_names())

    data = None
    with engine.connect() as connection:
        df = pd.read_sql("game", connection)
        print(df.head())
        data = df.head(10)
        data.drop(
            columns=["short_description", "supported_languages", "header_image"],
            axis=1,
            inplace=True,
        )
    data_for_plt = data.head()
    return render_template(
        "index.html", tables=[data.to_html(classes="data")], titles=data.columns.values,dataframe = data
    )

# @app.route('/fig/')
# def fig():
#       # plt.plot([1,2,3,4], [1,2,3,4])
#       plt.pie(data_for_plt['is_free'])
#       img = BytesIO()
#       plt.savefig(img)
#       img.seek(0)
#       return send_file(img, mimetype='image/png')
      
if __name__ == "__main__":
    app.run(debug=True)
