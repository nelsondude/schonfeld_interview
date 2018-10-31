import csv
import datetime
import os
import fileinput


TRADES_FILE_PATH = 'data/trades.csv'
SELL = 'sell'
BUY = 'buy'
FILLED = 'filled'
OPEN = 'open'


class Trade:

    def __init__(self, trader_id):
        self.trader_id = trader_id

    def getUpdateTrades(self, ticker, quantity, orderType):
        # We know this is open trade since its new
        # Also dont care about when it was placed since its most recent anyways
        trades_to_update = {}
        total_sell_quantity = 0
        with open(TRADES_FILE_PATH, 'r') as f:
            for i, line in enumerate(f):  # l == line
                l_id, l_ticker, l_quantity, l_type, l_date, l_status = line.strip().split(';')
                if l_id == self.trader_id or l_status == FILLED or l_ticker != ticker:  # skip if these conditions met
                    continue
                if orderType == SELL and l_type == BUY and l_quantity <= quantity:
                    # if quantity of buy is less than the quantity of the sell, we can fulfill the buy
                    quantity -= l_quantity
                    trades_to_update[l_id, l_date] = l_quantity
                    # uniquely identifies a trade, must make status == 'filled'

                elif orderType == BUY and l_type == SELL and total_sell_quantity < quantity:
                    trades_to_update[l_id, l_date] = l_quantity - max(0, total_sell_quantity - l_quantity)
                    # update quantity if partial sell order was filled
                    total_sell_quantity += l_quantity

            if orderType == SELL:
                return trades_to_update
            elif orderType == BUY and total_sell_quantity >= quantity:  # found enough open sells to fulfill the buy
                return trades_to_update
            else:
                return {}  # cant update any trades right now

    # def updateTradesFile(self, trades):
    #     for line in fileinput.input(TRADES_FILE_PATH, inplace=True):
    #         l_id, l_ticker, l_quantity, l_type, l_date, l_status = line.strip().split(';')
    #         if (l_id, l_date, ) in trades:
    #             print(";".join([l_id, l_ticker, trades[l_id, l_date], l_type, l_date, 'filled']))
    #         else:
    #             print(line)

    def writeToTradesFile(self, orders):
        now = datetime.datetime.now()
        append_write = 'a' if os.path.exists(TRADES_FILE_PATH) else 'w'
        with open(TRADES_FILE_PATH, append_write, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for order in orders:
                # all new trades are by default open
                ticker = order.get('symbol')
                quantity = order.get('quantity')
                orderType = order.get('orderType')
                trades_to_update = self.getUpdateTrades(ticker, quantity, orderType)
                status = 'filled' if bool(trades_to_update) else 'open'
                writer.writerow([self.trader_id, ticker, quantity, orderType, now, status])
                # self.updateTradesFile(trades_to_update)

    def getTradesForTrader(self):
        trades = []
        with open(TRADES_FILE_PATH, 'r') as csvfile:
            for i, line in enumerate(csvfile):
                t_id, symbol, quantity, orderType, timePlaced, status = line.strip().split(';')
                if t_id == self.trader_id:
                    trades.append({
                        'symbol': symbol,
                        'quantity': int(quantity),
                        'orderType': orderType,
                        'orderTime': str(timePlaced),
                        'status': status
                    })
        return trades

