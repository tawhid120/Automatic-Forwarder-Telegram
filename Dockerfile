# Use a slim version for faster builds and smaller image size
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for some python packages (like tgcrypto/numpy)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variable for PORT (Default 8080)
ENV PORT=8080

# Command to run the application using our new app.py
CMD ["python", "app.py"]


