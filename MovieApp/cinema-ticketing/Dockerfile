# Alegem imaginea de bază Python
FROM python:3.9-slim

# Setăm directorul de lucru în container
WORKDIR /app

# Copiem requirements.txt în container
COPY requirements.txt .

# Instalăm dependențele
RUN pip install -r requirements.txt

# Copiem aplicația Flask în container
COPY . .

# Expunem portul 5000 pentru aplicație
EXPOSE 5000

# Comanda pentru a porni aplicația Flask
CMD ["python", "app.py"]
