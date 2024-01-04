FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app
CMD gunicorn --bind 0.0.0.0:8000  --workers=2 app.main:app