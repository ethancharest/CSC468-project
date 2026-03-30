# Slim version of Base Python image. smaller size means faster build time.
FROM python:3.11-slim

# Commands run from here
WORKDIR /app

# Copy requirements to cache the pip install 
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install curl and clean apt cache
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .

# Make entrypoint executable (old code from test, can be removed)
RUN chmod +x entrypoint.sh

# Port 5000 is where Flask listens internally
EXPOSE 5000

# Flask app Entrypoint
ENV FLASK_APP=app.py

# Start Flask on container boot
CMD ["python", "app.py"]
