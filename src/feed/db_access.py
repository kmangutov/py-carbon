import aiosqlite
import datetime
import asyncio
import os


# Scale sqlite: https://stackoverflow.com/questions/784173/what-are-the-performance-characteristics-of-sqlite-with-very-large-database-file
SQL_CREATE_CANDLES = """CREATE TABLE IF NOT EXISTS Candles (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    timestamp_sql TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    timestamp_exchange INTEGER,
    exchange VARCHAR(16),
    symbol VARCHAR(16),
    asset_type VARCHAR(8),
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT
)"""


SQL_INSERT_CANDLE = """
INSERT INTO Candles(timestamp_exchange, exchange, symbol, asset_type, open, high, low, close, volume)
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


async def build_table_candles(db):
    cursor = await db.execute(SQL_CREATE_CANDLES)
    await cursor.close()

async def insert_candle(db,
                        exchange,
                        symbol,
                        asset_type,
                        candle):
    candle_tuple = (
        candle[0][0],
        exchange,
        symbol,
        asset_type,
        candle[0][1],
        candle[0][2],
        candle[0][3],
        candle[0][4],
        candle[0][5]
    )

    print(SQL_INSERT_CANDLE)
    print(candle_tuple)

    cursor = await db.execute(SQL_INSERT_CANDLE, candle_tuple)
    await db.commit()
    await cursor.close()
    

async def connect(dbpath):

    print('cwd: ', os.getcwd())
    #if not os.path.exists(dbpath):
    #    os.makedirs(dbpath)

    if not os.path.exists(dbpath):
        open(dbpath, 'w').close()

    db = await aiosqlite.connect(dbpath)
    await build_table_candles(db)
    return db


async def main():
    db = await connect()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())