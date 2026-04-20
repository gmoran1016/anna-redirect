FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir Flask==3.0.3 requests==2.32.3 beautifulsoup4==4.12.3 gunicorn==22.0.0

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "30", "app:app"]
