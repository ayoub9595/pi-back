# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose port 5001
EXPOSE 5001

# Set Flask to run on port 5001
ENV FLASK_RUN_PORT=5001

# Run the application using flask run command
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]