# Start from the official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first so Docker can cache this layer
# (only re-runs pip install if requirements.txt changes)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code into the container
COPY . .

# Expose port 5000 so other containers can reach Flask
EXPOSE 5000

# Command to run the Flask app when the container starts
CMD ["python", "app.py"]
