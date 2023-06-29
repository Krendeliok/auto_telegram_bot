FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN echo "Y" | apt-get upgrade

RUN echo "Y" | apt-get install cron
RUN apt-get install nano

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN echo "0 8 * * * python3 /app/send_advertisement.py" | crontab

CMD ["python", "main.py"]
