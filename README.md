# py-carbon

### Description

Pricefeed using CCXT / CCXTPro. Connect to Binance BTC/USDT spot and futures and write updates to sqlite file.

### Running

Run locally:
```bash
pip3 install -r requirements.txt
python3 ./src/feed/spot_future_feed.py
```

Build and run docker, with example local volume:
```bash
docker build -t spot_future_feed .
docker run -v /Users/kmangutov/dev/py-carbon/volume:/code/data spot_future_feed
```
