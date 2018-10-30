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
            writer.writerow([trader_id, order.get('symbol'), order.get('quantity'), order.get('orderType'), now])
