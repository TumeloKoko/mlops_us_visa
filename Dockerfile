# Use a small, production-ready Python image
FROM python:3.8.5-slim-buster

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt  /app/

# Install dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /app

# Run the FastAPI app via Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
