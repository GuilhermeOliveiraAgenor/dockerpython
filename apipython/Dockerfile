FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask sqlalchemy redis requests flask-sqlalchemy mysql-connector-python gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
