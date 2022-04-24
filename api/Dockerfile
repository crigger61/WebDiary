FROM python:3.9-buster

WORKDIR /app

RUN pip install --upgrade pip wheel
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python app.py