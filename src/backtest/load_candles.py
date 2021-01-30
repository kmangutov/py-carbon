# Load OHLCV from sqlite and convert to pandas or cerebro/backtrader format.

import sqlite3
import backtrader as bt
import backtrader.feeds as btfeed
import pandas as pd
import datetime

# Tick data and bid/ask for backtrader: https://www.backtrader.com/blog/posts/2016-03-08-escape-from-ohlc-land/escape-from-ohlc-land/

# Didn't figure out how to use relative directory, since this code is going to be called from Jupyter
# conn = sqlite3.connect('./data/ts.db')
conn = sqlite3.connect('/Users/kmangutov/dev/py-carbon/data/nopro.db')

def sample():
    c = conn.cursor()
    rows = c.execute('SELECT * FROM Candles ORDER BY id DESC LIMIT 1000')
    for row in rows:
        print(row)
    return rows

def sample_df():
    c = conn.cursor()
    rows = c.execute('SELECT * FROM Candles ORDER BY id DESC LIMIT 1000')
    df = pd.DataFrame()

    for row in rows:

        _open = row[6]
        _high = row[7]
        _low = row[8]
        _close = row[9]
        _volume = row[10]
        _timestamp = row[1]
        _id = row[0]

        # TODO: Debug this part to use right datetime formats
        log_dt = datetime.datetime.strptime(_timestamp, "%Y-%m-%d %H:%M:%S")

        d = {
            'datetime': log_dt,#_unix,
            'open': _open,
            'high': _high,
            'low': _low,
            'close': _close,
            'volume': _volume,
            'id': _id,
        }
        
        frame = pd.DataFrame(data=d, index=[0])
        df = df.append(frame)
    df.set_index('datetime', inplace=True)
    return df

def sample_cerebro():
    return bt.feeds.PandasData(dataname=sample_df(), timeframe=bt.TimeFrame.Ticks)
