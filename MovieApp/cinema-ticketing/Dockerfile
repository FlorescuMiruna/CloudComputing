# Folosește o imagine de bază Python
FROM python:3.9-slim

# Setează directorul de lucru
WORKDIR /app

# Copiază fișierele necesare
COPY . /app

# Instalează dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Expune portul 5000
EXPOSE 5000

# Comanda pentru a rula aplicația Flask
CMD ["python", "app.py"]
