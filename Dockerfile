FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt alembic.ini ./
COPY .env ./
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
EXPOSE 8000

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
