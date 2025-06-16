FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install flask psycopg2

EXPOSE 5002

CMD ["python", "app.py"]
