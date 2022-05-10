FROM python:3.8.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app

RUN chmod +x /app/run_test.sh