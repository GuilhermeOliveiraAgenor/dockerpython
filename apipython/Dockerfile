FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask sqlalchemy redis requests flask-sqlalchemy mysql-connector-python

EXPOSE 8000

CMD ["python", "app.py"]
