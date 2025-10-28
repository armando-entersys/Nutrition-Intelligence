#!/bin/bash

# Production Deployment Script for Nutrition Intelligence
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
PROJECT_NAME="nutrition-intelligence"
DOCKER_COMPOSE_FILE="docker-compose.production.yml"

echo "=============================================="
echo "Deploying Nutrition Intelligence to $ENVIRONMENT"
echo "=============================================="

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# Load environment variables
if [ -f ".env.${ENVIRONMENT}" ]; then
    echo "Loading environment variables from .env.${ENVIRONMENT}"
    export $(cat .env.${ENVIRONMENT} | xargs)
else
    echo "Warning: .env.${ENVIRONMENT} file not found. Using default values."
fi

# Validate required environment variables
required_vars=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASSWORD" "SECRET_KEY" "REDIS_PASSWORD" "MINIO_ACCESS_KEY" "MINIO_SECRET_KEY")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

echo "Environment validation passed"

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs static ssl

# Backup existing data (if any)
if docker volume ls | grep -q "${PROJECT_NAME}_postgres_data_prod"; then
    echo "Creating backup of existing data..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    docker run --rm -v ${PROJECT_NAME}_postgres_data_prod:/data -v $(pwd)/backups:/backup alpine \
        tar czf /backup/postgres_backup_${timestamp}.tar.gz -C /data .
    echo "Backup created: backups/postgres_backup_${timestamp}.tar.gz"
fi

# Pull latest images
echo "Pulling latest Docker images..."
docker-compose -f $DOCKER_COMPOSE_FILE pull

# Build custom images
echo "Building application images..."
docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f $DOCKER_COMPOSE_FILE down

# Start services
echo "Starting services..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
timeout=300
elapsed=0

while [ $elapsed -lt $timeout ]; do
    if docker-compose -f $DOCKER_COMPOSE_FILE ps | grep -q "healthy"; then
        echo "Services are starting..."
        sleep 5
        elapsed=$((elapsed + 5))
    else
        break
    fi
done

# Check service status
echo "Checking service status..."
docker-compose -f $DOCKER_COMPOSE_FILE ps

# Run health checks
echo "Running health checks..."
echo "Checking backend health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

echo "Checking frontend..."
if curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend accessibility check failed"
fi

# Display deployment information
echo "=============================================="
echo "Deployment completed!"
echo "=============================================="
echo "Frontend URL: http://localhost"
echo "API URL: http://localhost/api"
echo "API Documentation: http://localhost/docs"
echo "MinIO Console: http://localhost:9001"
echo ""
echo "Container status:"
docker-compose -f $DOCKER_COMPOSE_FILE ps

echo ""
echo "To monitor logs:"
echo "  docker-compose -f $DOCKER_COMPOSE_FILE logs -f"
echo ""
echo "To stop all services:"
echo "  docker-compose -f $DOCKER_COMPOSE_FILE down"
echo ""
echo "To remove all data (including volumes):"
echo "  docker-compose -f $DOCKER_COMPOSE_FILE down -v"