FROM 3.7.8-alpine

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt