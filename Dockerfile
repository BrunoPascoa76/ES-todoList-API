FROM python:3.13
COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /app

WORKDIR /app

CMD ["python3","-m","flask","run","--debug","--host=0.0.0.0"]