FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Carpeta para el volumen persistente de SQLite (Unidad III: Almacenamiento)
RUN mkdir -p /data
ENV DB_PATH=/data/notas.db

EXPOSE 5000

CMD ["python", "app.py"]
