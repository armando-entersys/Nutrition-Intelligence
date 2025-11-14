# Backend Dockerfile for Nutrition Intelligence
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including logrotate
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    logrotate \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for SQLite database and logs
RUN mkdir -p /app/data /app/logs && \
    chmod 755 /app/logs

# Copy logrotate configuration
COPY logrotate.conf /etc/logrotate.d/nutrition-intelligence
RUN chmod 644 /etc/logrotate.d/nutrition-intelligence

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
