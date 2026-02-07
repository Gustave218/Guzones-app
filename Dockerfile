# Use a stable Python version (Fly.io friendly)
FROM python:3.12-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /code

# System dependencies (optional but recommended)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
RUN pip install Flask-Login

# Copy project files
COPY . .

# Fly.io listens on 8080
EXPOSE 8080

# Run Flask with Gunicorn (your original)
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:8080"]