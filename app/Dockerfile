FROM python:3.7.8-slim-buster

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apt-get update -y 
RUN apt-get install libgtk2.0-dev -y

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN export FLASK_APP=app.py

EXPOSE 5000

CMD ["python3", "app.py"] 
