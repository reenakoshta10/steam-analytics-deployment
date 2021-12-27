import os

import sqlalchemy
from steam_analytics import calculate_unit_sold
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import matplotlib.pyplot as plt

def connect_get_data():
  with engine.connect() as connection:
      df = pd.read_sql("game", connection)
      df['year_of_release'] = df["release_date"].apply(lambda d: int(d[-4:]))  
      df['unit_sold'] = df.apply(lambda x: calculate_unit_sold(x.total_reviews, x.year_of_release), axis= 1)
      df['revenue'] = df['unit_sold']* df["price_USD"] 
  return df

def get_df_for_genres():
  glist = []
  for x in df[df.genres.notnull()]['genres']:
    a = x.split(', ')
    for n in a:
      if n not in glist:
        glist.append(n)
  genres_df= pd.DataFrame(columns=glist)
  for sub in df[df.genres.notnull()]['genres']:
    genres_df.loc[len(genres_df)] = 0
    a = sub.split(', ')
    for x in a:
      genres_df.loc[len(genres_df)-1][x] = 1
  genres_df["id"] = df["id"]
  genres_df["revenue"] = df["revenue"]
  genres_df["unit_sold"] = df["unit_sold"]
  return genres_df, glist

def get_top_games(x_val, y_val, count):
  
  data= df.sort_values(by =[y_val],ascending=False)
  data = data.head(count)
  fig = px.bar(data, x= x_val,y = y_val, color= x_val, title = f"Top {count} Games based on {dictionary[y_val]}", 
  hover_data=[x_val, y_val], 
             labels={x_val:'Game', y_val:dictionary[y_val]}, 
             width = 1000, height=700)
  return fig

def get_fig_by_year( y_val):
  data= df.groupby('year_of_release')[y_val].sum()
  # data = data.head(count)
  
  fig = px.bar(data, x= data.index.values,y = data.values, color= data.index.values, title = f"Yearwise {dictionary[y_val]} for Steam games", 
  hover_data=[data.index.values, data.values], 
             labels=dict(x=dictionary['year_of_release'], y=dictionary[y_val], color="Year"), 
             width = 1000, height=700)
  return fig

def get_fig_by_genres(y_val, count):
  genres_rev=[]
  for col in glist:
    genres_rev.append({"genre": col, "revenue" : genres_df[genres_df[col]==1]['revenue'].sum(), 
    "unit_sold" : genres_df[genres_df[col]==1]['unit_sold'].sum()})

  genres_rev = pd.DataFrame(genres_rev)
  genres_rev = genres_rev.sort_values(by =[y_val],ascending=False)
  genres_rev = genres_rev.head(count)
  
  fig = px.bar(genres_rev, x= 'genre',y = y_val, color= 'genre', title = "Revenue based on Genres", 
              hover_data=['genre',y_val], 
              labels=dict(x="Genres", y=dictionary[y_val]), 
              width = 1000, height=700)
  return fig

app = dash.Dash(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "../data/gamedatabase.db")
)
engine = sqlalchemy.create_engine(database_file)
df = connect_get_data()
genres_df, glist = get_df_for_genres()
dictionary = {
  'revenue': 'Revenue',
  'unit_sold': 'Unit Sold',
  'genres': "Genres",
  'year_of_release': "Year of Release"
}

app.layout = html.Div(children=[
    
      html.H1(children = "Steam Analytics", style = {'textAlign':'center'}),
      html.Div([
          html.Div(children=[
              html.Label('X axis values'),
              dcc.Dropdown(
                  id = 'x_val',
                  options=[
                      {'label': 'Game Names', 'value': 'name'},
                      {'label': 'Genres', 'value': 'genres'},
                      {'label': 'Year', 'value': 'year'}
                  ],
                  value='name'
              ),

              html.Br(),
              html.Label('Y axis values'),
              dcc.Dropdown(
                  id = 'y_val',
                  options=[
                      {'label': 'Revenue', 'value': 'revenue'},
                      {'label': 'Unit Sold', 'value': 'unit_sold'},
                  ],
                  value='revenue',
              ),

              html.Br(),
              html.Label('Record Count'),
              dcc.RadioItems(
                  id = 'record_count',
                  options=[
                      {'label': 'Top 10', 'value': 10},
                      {'label': u'Top 25', 'value': 25},
                      {'label': 'Top 50', 'value': 50}
                  ],
                  value=10,
                  labelStyle={'display': 'flex'}
              ),
          ], style={'padding': 10, 'width': '25%'}),

          html.Div(children=[
              dcc.Graph(
              id='graph',
              # figure=fig, 
              style={'align': 'center'}
              
            )
          ], style={'padding': 10, 'width': '75%', 'margin-left':'100px'})
      ], style={'display': 'flex', 'flex-direction': 'row'})
])

@app.callback(
    Output('graph', 'figure'),
    Input('x_val', 'value'),
    Input('y_val', 'value'),
    Input('record_count','value'))
def get_fig(x_val, y_val, count):
    if x_val == 'year':
      fig = get_fig_by_year(y_val)
    elif x_val == 'genres':
      fig = get_fig_by_genres(y_val, count)
    else:
      fig = get_top_games(x_val, y_val, count)
    return fig


if __name__ == '__main__':
    port = os.environ.get('PORT') if os.environ.get('PORT') is not None else 5000
    print("PORT:",port)

    app.run_server(host = "0.0.0.0", port = port, debug=True)