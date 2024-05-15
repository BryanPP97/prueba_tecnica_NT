# Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "if [ \"$APP_MODE\" = 'api' ]; then uvicorn api.main:app --host 0.0.0.0 --port 8000; else python etl/data_etl.py; fi"]

