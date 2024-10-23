from flask import Flask, render_template
import pandas as pd
import backtrader as bt
app = Flask(__name__)




@app.route('/')
def index():
    
    cerebro = bt.Cerebro()
    # ################################
    # Prepare your steps for cerebro.run(), just as the original steps
    # Your strategy should inherit OrderTracker and it will automatically save the order history for plot
    # 
    #  Your code here 
    #  
    # ################################
    results = cerebro.run()
    stra = results[0]
    order_df = stra.get_order_history()
    
    # this df should be your input data, Where Date in format of '%Y-%m-%d', and has column open, high,close,low
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    
    order_df['Date'] = pd.to_datetime(order_df['Date']).dt.strftime('%Y-%m-%d')

    return render_template('index.html',
                           price_data=df.to_dict(orient='records'),
                           order_data=order_df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
