FROM python:3.10-slim-buster as builder
LABEL authors="Hamed Babaei Giglou"

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "flask_app.py", "runserver", "0.0.0.0:6003"]
