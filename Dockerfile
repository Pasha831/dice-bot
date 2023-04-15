FROM python:3.9-slim as compiler

WORKDIR /app/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
