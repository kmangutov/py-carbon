FROM python:3.8-slim

VOLUME ["/code/data/"]

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

CMD ["python3", "./feed/spot_future_feed.py", "--dbpath", "/code/data/ts.db"]