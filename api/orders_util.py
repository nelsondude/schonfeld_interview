import csv
import datetime
import os


TRADES_FILE_PATH = 'data/trades.csv'


def writeToTradesFile(trader_id, orders):
    now = datetime.datetime.now()
    append_write = 'a' if os.path.exists(TRADES_FILE_PATH) else 'w'
    with open(TRADES_FILE_PATH, append_write, newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for order in orders:
            # all new trades are by default open
            writer.writerow([trader_id, order.get('symbol'), order.get('quantity'), order.get('orderType'), now, 'open'])


def getTradesForTrader(trader_id):
    trades = []
    with open(TRADES_FILE_PATH, 'r') as csvfile:
        for i, line in enumerate(csvfile):
            t_id, symbol, quantity, orderType, timePlaced, status = line.strip().split(';')
            if t_id == trader_id:
                trades.append({
                    'symbol': symbol,
                    'quantity': int(quantity),
                    'orderType': orderType,
                    'orderTime': str(timePlaced),
                    'status': status
                })
    return trades

