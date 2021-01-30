# py-carbon

### Description

Pricefeed using CCXT / CCXTPro. Connect to Binance BTC/USDT spot and futures and write updates to sqlite file.

### Running

Run locally:
```bash
pip3 install -r requirements.txt
python3 ./src/feed/spot_future_feed.py
```


### Virtual Environment

Virtual Environment (venv, https://docs.python.org/3/tutorial/venv.html) can be used to manage dependencies.

Create venv for current folder:
```bash
python3 -m venv .venv
```

Activate venv:
```bash
source .venv/bin/activate
```

Now you can use pip3 install and run locally script:
Run locally:
```bash
pip3 install -r requirements.txt
python3 ./src/feed/spot_future_feed.py
```



### Docker

Experimental: Build and run docker, with example local volume:
```bash
docker build -t spot_future_feed .
docker run -v /Users/kmangutov/dev/py-carbon/volume:/code/data spot_future_feed
```
