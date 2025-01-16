# Dockerfile pentru cinema-service
FROM python:3.9-slim

# Setăm directorul de lucru
WORKDIR /app

# Copiem fișierele necesare în container
COPY requirements.txt /app/

# Instalăm dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Copiem aplicația în container
COPY . /app/

# Setăm portul pe care rulează aplicația
EXPOSE 5000

# Comanda de rulare a aplicației
CMD ["python", "app.py"]
