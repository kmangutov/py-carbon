# py-carbon

Run locally:
python3 ./src/feed/spot_future_feed.py

Build and run docker:
docker build -t spot_future_feed .
docker run -v ./volume/:/code/data spot_future_feed