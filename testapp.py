from flask import Flask, render_template
import pandas as pd
import backtrader as bt
import strategy.MACDStrategy as macd
app = Flask(__name__)


def test_on_one_american_stock(df, strategy, name):
    print(f'Back Trade on {name}.')
    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter data for the date range 2020-01-01 to 2024-01-01
    start_date = '2020-01-01'
    end_date = '2024-10-21'
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Set the 'Date' column as the DataFrame index
    df.set_index('Date', inplace=True)

    # Pass the data to the backtrader data feed and add it to Cerebro
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,  # No need to specify if Date is already the index
        open='Open',
        high='High',
        low='Low',
        close='Close',
        volume='Volume',
        openinterest=-1  # Set to -1 if open interest is not available
    )

    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy)
    cerebro.adddata(data)

    # Set starting cash
    cerebro.broker.setcash(100000.0)

    start_cash = cerebro.broker.getvalue()

    # Run the strategy
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    result= cerebro.run()
    # Get the strategy instance
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    end_cash = cerebro.broker.getvalue()
    rate = (end_cash - start_cash) * 100 / start_cash
    print(f'Rate:{rate:.2f}%')
    return result


@app.route('/')
def index():
    df = pd.read_csv('./data/american_indices/^GSPC.csv')
    start_date = '2020-01-01'
    end_date = '2024-10-21'
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    results = test_on_one_american_stock(df,macd.MACDStrategy,'SP500')
    stra = results[0]
    order_df = stra.get_order_history()
    # Convert 'Date' to string for rendering in the frontend
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    order_df['Date'] = pd.to_datetime(order_df['Date']).dt.strftime('%Y-%m-%d')

    # Pass data to the template for visualization
    return render_template('test_light_chart.html',
                           price_data=df.to_dict(orient='records'),
                           order_data=order_df.to_dict(orient='records'))



if __name__ == '__main__':
    app.run(debug=True)