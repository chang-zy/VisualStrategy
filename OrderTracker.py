import backtrader as bt
import pandas as pd

class OrderTracker(bt.Strategy):
    def __init__(self):
        self.order_history = []  # Initialize to store buy/sell orders

    def notify_order(self, order):
        if order.status in [order.Completed]:
            # Track every order (buy/sell) when it's completed
            if order.isbuy():
                order_type = 'BUY'
            elif order.issell():
                order_type = 'SELL'

            # Save order information when it's completed
            order_info = {
                'Date': bt.num2date(order.executed.dt).strftime("%Y-%m-%d"),
                'Order Type': order_type,
                'Size': order.executed.size,
                'Price': order.executed.price,
                'Commission': order.executed.comm,
            }
            self.order_history.append(order_info)

    def get_order_history(self):
        return pd.DataFrame(self.order_history)