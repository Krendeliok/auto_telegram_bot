FROM python:3.10 AS build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /website

RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gettext curl graphviz \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir --resume-retries 5 -r requirements.txt

COPY . .

EXPOSE 5000