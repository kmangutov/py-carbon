# -*- coding: utf-8 -*-

import argparse
import db_access
import asyncio
import time
import datetime

USE_PRO = False
if USE_PRO: 
    import ccxtpro
else:
    import ccxt as ccxtpro


STRING_EXCHANGE = 'binance'

# Multiple exchanges: https://github.com/ccxt/ccxt/blob/master/examples/py/async-orderbooks-from-multiple-exchanges-at-once.py
# Spot vs future: https://github.com/ccxt/ccxt/blob/master/examples/py/async-binance-futures-vs-spot.py
    
async def loop(db, exchange, symbol, asset_type):
    while True:
        try:
            exchange.options['defaultType'] = asset_type
            
            candle = []
            if USE_PRO:
                candle = await exchange.watch_ohlcv(symbol)
            else:
                time.sleep(1.0)#exchange.rateLimit / 1000) # time.sleep wants seconds
                #since = datetime.datetime.now() - datetime.timedelta(minutes=1)
                candle = exchange.fetch_ohlcv(symbol, timeframe='1m')#, since=since.timestamp())
                candle = [candle[len(candle) - 1]] # Put in array so its backwards compatible with watch_ohlcv

            now = exchange.milliseconds()
            print(exchange.iso8601(now), STRING_EXCHANGE, symbol, asset_type, symbol, candle)#orderbook['asks'][0], orderbook['bids'][0])
            await db_access.insert_candle(db, STRING_EXCHANGE, symbol, asset_type, candle)
        except Exception as e:
            print(str(e))
            # raise e  # uncomment to break all loops in case of an error in any one of them
            # break  # you can also break just this one loop if it fails


# TODO: USE_PRO=True works but for USE_PRO=False CCXT, need separate spot and future instanes
# with exchange.options['defaultType'] = asset_type.
async def main():
    parser = argparse.ArgumentParser("spot_future_feed")
    parser.add_argument("--dbpath", help="Database path.", type=str, default='./data/ts.db')
    args = parser.parse_args()
    print(args.dbpath)

    db = await db_access.connect(args.dbpath)

    exchange = ccxtpro.binance({'enableRateLimit': True})

    symbols = ['BTC/USDT']
    asset_types = ['spot', 'future']
    await asyncio.gather(*[loop(db, exchange, symbol, asset_type) for symbol in symbols for asset_type in asset_types])
    await exchange.close()
    await db.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())