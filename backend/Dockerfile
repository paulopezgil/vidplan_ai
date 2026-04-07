FROM python:3.11-slim

# Create app directory
WORKDIR /app

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory to /app/backend
COPY . /app/backend

WORKDIR /app

# Add backend directory to Python path
ENV PYTHONPATH=/app/backend:$PYTHONPATH

EXPOSE 8000

# Run the app from the backend module
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
