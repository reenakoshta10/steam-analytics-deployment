import os
import pandas as pd

from flask import Flask
from flask import render_template
from flask import request

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

import matplotlib.pyplot as plt

app = Flask(__name__)


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

    return render_template(
        "index.html", tables=[data.to_html(classes="data")], titles=data.columns.values
    )


if __name__ == "__main__":
    app.run(debug=True)
