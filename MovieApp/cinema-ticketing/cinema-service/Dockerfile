FROM python:slim
WORKDIR /app

# Actualizare și instalare PostgreSQL client
RUN apt update && apt install -y postgresql-client

# Copiere și instalare dependențe
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copierea codului aplicației în container
COPY . .

# Pornirea aplicației folosind Gunicorn
ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
