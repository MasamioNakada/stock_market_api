FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=8080 >> api.txt"]