import csv
import datetime
import fileinput
import os

TRADES_FILE_PATH = 'data/trades.csv'
SELL = 'sell'
BUY = 'buy'
FILLED = 'filled'
OPEN = 'open'


class TradeLine:  # Converts a line from the text file to an object of useful data
    def __init__(self, line_string):
        trader_id, ticker, quantity, amount_left, order_type, date_placed = line_string.strip().split(';')
        self.trader_id = trader_id
        self.ticker = ticker
        self.quantity = int(quantity)
        self.amount_left = int(amount_left)  # initially all is available for trade
        self.date_placed = date_placed
        self.order_type = order_type
        self.status = 'filled' if amount_left == 0 else 'open'

    def formatted(self):
        return ";".join(
            [self.trader_id, self.ticker, str(self.quantity), str(self.amount_left), self.order_type, self.date_placed])

    @staticmethod
    def format(trader_id, ticker, quantity, amount_left, order_type, date_placed):
        return ";".join([trader_id, ticker, str(quantity), str(amount_left), order_type, str(date_placed)])

    def get_trade_dict(self):
        return {
            'symbol': self.ticker,
            'quantity': int(self.quantity),
            'orderType': self.order_type,
            'orderTime': self.date_placed,
            'status': 'filled' if self.amount_left == 0 else 'open'
        }

    def attributes(self):
        return [self.trader_id, self.ticker, self.quantity, self.amount_left, self.order_type, self.date_placed]

    def __repr__(self):
        return self.formatted()

    def __str__(self):
        return self.formatted()


class Trade:

    def __init__(self, trader_id):
        self.trader_id = trader_id

    def get_update_trades(self, ticker, quantity, orderType):
        trades = []
        with open(TRADES_FILE_PATH, 'r') as f:
            for i, line in enumerate(f):  # l == line
                tl = TradeLine(line)
                if tl.trader_id == self.trader_id or tl.status == FILLED or tl.ticker != ticker:
                    # skip if these conditions met
                    pass
                elif orderType != tl.order_type:  # Buy/Sell or Sell/Buy
                    diff = min(quantity, tl.amount_left)
                    quantity -= diff
                    tl.amount_left -= diff
                trades.append(tl)
        return trades, quantity

    @staticmethod
    def update_trades_file(trades):
        # Update all lines in the text file with updated TradeLine objects
        with fileinput.input(TRADES_FILE_PATH, inplace=True) as f:
            for i, line in enumerate(f):
                print(trades[i].formatted())

    def write_to_trades_file(self, orders):
        """Goes through each order submitted by a user. After updating all orders in the text file,
        then write the order to the end of the file"""
        now = datetime.datetime.now()
        append_write = 'a' if os.path.exists(TRADES_FILE_PATH) else 'w'

        # Open and close it so that it saves
        csvfile = open(TRADES_FILE_PATH, append_write, newline='')
        csvfile.close()

        for order in orders:
            # Get order variables
            ticker = order.get('symbol')
            quantity = int(order.get('quantity'))
            order_type = order.get('orderType')

            # Update the old trades first
            new_trades, new_quantity = self.get_update_trades(ticker, quantity, order_type)
            self.update_trades_file(new_trades)

            # Open and write a line to the file
            csvfile = open(TRADES_FILE_PATH, append_write, newline='')
            writer = csv.writer(csvfile)
            line = TradeLine.format(self.trader_id, ticker, quantity, new_quantity, order_type, now)
            writer.writerow([line])
            csvfile.close()

    def get_trades_for_trader(self):
        trades = []
        with open(TRADES_FILE_PATH, 'r') as f:
            for i, line in enumerate(f):
                trade = TradeLine(line)
                if self.trader_id == trade.trader_id:
                    trades.append(trade.get_trade_dict())
        return trades
