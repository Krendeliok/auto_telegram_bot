FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN echo "Y" | apt-get upgrade

RUN echo "Y" | apt-get install cron
RUN apt-get install nano

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
