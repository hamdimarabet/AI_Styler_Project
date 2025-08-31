# Use an official Python image with Linux compatibility
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install system dependencies for Mediapipe
RUN apt-get update && \
    apt-get install -y build-essential cmake pkg-config libatlas-base-dev libgl1-mesa-glx libglib2.0-0 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose port
EXPOSE 10000

# Command to run Gunicorn using Render's PORT
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "2"]
