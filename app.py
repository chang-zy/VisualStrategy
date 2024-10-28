import os

from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)


def search_name(file_name):
    df = pd.read_csv('tushare_stock_basic_20241028103249.csv')
    file_name = file_name.split('.')[0]

    # Check if `file_name` is in the 'ts_code' column
    for i in range(len(df)):
        if file_name in df.loc[i, 'ts_code']:
            return df.loc[i, 'name']

    return None  # Return None if the file_name is not found



# Load your data (assume data is stored as 'data.csv' in the same directory)
def load_data(symbol):
    # Replace 'data.csv' with your actual CSV path
    data = pd.read_csv(f'./data/{symbol}')
    data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
    data = data.iloc[::-1]
    name = search_name('002060.SZ.csv')
    return name,data

@app.route('/')
def index():
    symbol_list= os.listdir('./data')
    stocks = [{"name":search_name(x),"symbol":x} for x in symbol_list]
    # Example stock list, each stock has a name and a unique identifier

    return render_template('index.html', stocks=stocks)

@app.route('/stock/<symbol>')
def stockInfo(symbol):
    name,df = load_data(symbol)
    data = []
    # 遍历df
    # Convert 'time' to datetime format and reformat it
    for index,row in df.iterrows():
        data.append({"time":str(row['trade_date']),
                     "open": float(row['open']),
                     "high":float(row['high']),
                     "low":float(row['low']),
                     "close":float(row['close'])})

    # Pass the data to the template
    return render_template('stockInfo.html', name=name,data=data)

if __name__ == '__main__':
    app.run(debug=True)