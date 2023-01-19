# import pandas as pd
# import plotly.express as px  # (version 4.7.0 or higher)
# import plotly.graph_objects as go
# from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from sqlite3 import Timestamp
import sys
import time
from zoneinfo import ZoneInfo
import dash
from dash import Dash, dcc, html, Input, Output 
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import date
# Get Historical Data 1
import requests
import csv
import json


# https://api.coincap.io/v2/assets/bitcoin/history?interval=d1&start=1670662322000&end=1673340722000

url = "http://api.coincap.io/v2/assets/bitcoin/history?interval=d1&start=1592585794000&end=1673749918000"
assets = "http://api.coincap.io/v2/assets"



payload = {}
headers = {}

response_1 = requests.request("GET", url, headers=headers, data = payload)
json_data_1 = json.loads(response_1.text.encode('utf8'))["data"]

# print(json_data_1)
response_2 = requests.request("GET", assets, headers=headers, data = payload)
json_data_2 = json.loads(response_2.text.encode('utf8'))["data"]
# print(json_data_2)


coins = []
for i in json_data_2:
    coins.append(i['id'])


print(coins)


prices = []
for i in json_data_1:
    prices.append(i['priceUsd'])

print(prices)


dates = []
for i in json_data_1:
    dates.append(i['date'])
  
times = []
for i in json_data_1:
    times.append(i['time'])

# dates = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('America/New_York')).strftime('%m-%d-%Y-%H-%S'), dates))










# Storing the data we want

# df = pd.DataFrame(json_data_1)
# df.to_csv('bitcoin-usd.csv', index=False)




# Removing obsolete data column
# df = pd.DataFrame(json_data_1, columns=['time', 'priceUsd'])
# print(df.sample)



# Identifying data types in our dataframe
# Converting 'priceUsd' data from type object to float 
# and 'date' from type object to datetime

# df['priceUsd'] = pd.to_numeric(df['priceUsd'], errors='coerce').fillna(0, downcast='infer')






# df.plot(x ='time', y='priceUsd', kind = 'line')
# plt.show()

# print(df.dtypes)
# print(df)




# datelist = datetime.strptime(dates,'%Y%m%d') 











app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Crypto Currency Dashboard with Dash", style={'text-align': 'center'}),
    
    
    dcc.Graph(id='graph'),

    dcc.Dropdown(coins, 'bitcoin', id='demo_dropdown'),
    
    
    html.Div(id='dd-output-container'),

    dcc.DatePickerRange(
        id='my-date-picker-range',
        calendar_orientation='vertical',
        day_size=39,
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2023, 9, 19),
        initial_visible_month=date(2022, 12, 10),
        start_date=dates[0],
        end_date=dates[-1]
    ),
    html.Div(id='output-container-date-picker-range')

    # dcc.Graph(id='my_bee_map', figure={})

])


@app.callback(
    Output("graph", "figure"),
    Input('demo_dropdown', 'value')
)

def update_output(value):
    response_1 = requests.request("GET", f"http://api.coincap.io/v2/assets/{value}/history?interval=d1&start=1592585794000&end=1673749918000", headers=headers, data = payload)
    json_data_1 = json.loads(response_1.text.encode('utf8'))['data']
    
    figure=px.bar(
        data_frame=json_data_1,
        x='priceUsd',
        y='date'
    )
    return figure


    

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('demo_dropdown', 'value')
)



def update_output(value, start_date, end_date):
    start_date = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('America/New_York')).strftime('%Y-%m-%d'), dates))
    end_date = list(map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('America/New_York')).strftime('%Y-%m-%d'), dates))
    response_1 = requests.request("GET", f"http://api.coincap.io/v2/assets/{value}/history?interval=d1&start={start_date}&end={end_date}", headers=headers, data = payload)
    json_data_1 = json.loads(response_1.text.encode('utf8'))['data']

    figure=px.bar(
        data_frame=json_data_1,
        x='priceUsd' > start_date,
        y='date'
    )
    return figure
    



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components



if __name__ == '__main__':
    app.run_server(debug=False)




