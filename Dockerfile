FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt alembic.ini ./
COPY .env ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
EXPOSE 8000

# Команда запуска uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
