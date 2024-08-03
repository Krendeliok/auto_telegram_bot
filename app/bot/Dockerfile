FROM python:3.10

WORKDIR /bot

RUN apt-get update
RUN echo "Y" | apt-get upgrade

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
