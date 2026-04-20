FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir Flask==3.0.3 requests==2.32.3 beautifulsoup4==4.12.3

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
