#!/bin/bash

# Production Deployment Script with Zero-Downtime
# Usage: ./scripts/deploy.sh [environment] [version]

set -e

ENVIRONMENT=${1:-production}
VERSION=${2:-latest}
PROJECT_NAME="nutrition-intelligence"

echo "=============================================="
echo "🚀 Deploying Nutrition Intelligence"
echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"
echo "=============================================="

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."

    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed"
        exit 1
    fi

    echo "✅ Prerequisites check passed"
}

# Load environment configuration
load_environment() {
    echo "🔧 Loading environment configuration..."

    ENV_FILE=".env.${ENVIRONMENT}"
    if [ -f "$ENV_FILE" ]; then
        export $(cat $ENV_FILE | xargs)
        echo "✅ Environment variables loaded from $ENV_FILE"
    else
        echo "⚠️ Warning: $ENV_FILE not found, using defaults"
    fi
}

# Validate required environment variables
validate_environment() {
    echo "🔍 Validating environment variables..."

    required_vars=(
        "POSTGRES_DB"
        "POSTGRES_USER"
        "POSTGRES_PASSWORD"
        "SECRET_KEY"
        "REDIS_PASSWORD"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "❌ Required environment variable $var is not set"
            exit 1
        fi
    done

    echo "✅ Environment validation passed"
}

# Create backup
create_backup() {
    echo "💾 Creating backup..."

    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR

    # Database backup
    if docker ps | grep -q "${PROJECT_NAME}-postgres"; then
        echo "Backing up database..."
        docker exec ${PROJECT_NAME}-postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_DIR/database.sql
        echo "✅ Database backup created: $BACKUP_DIR/database.sql"
    fi

    # Application backup
    if [ -d "logs" ]; then
        cp -r logs $BACKUP_DIR/
        echo "✅ Logs backed up"
    fi

    echo "✅ Backup completed: $BACKUP_DIR"
}

# Pull latest images
pull_images() {
    echo "📥 Pulling latest Docker images..."

    COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"
    docker-compose -f $COMPOSE_FILE pull

    echo "✅ Images pulled successfully"
}

# Health check function
health_check() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    echo "🏥 Performing health check for $service_name..."

    while [ $attempt -le $max_attempts ]; do
        if curl -f "$url" &> /dev/null; then
            echo "✅ $service_name is healthy"
            return 0
        fi

        echo "⏳ Waiting for $service_name... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    echo "❌ $service_name health check failed"
    return 1
}

# Blue-green deployment
blue_green_deploy() {
    echo "🔄 Starting blue-green deployment..."

    COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

    # Create new deployment (green)
    echo "🟢 Starting green deployment..."
    docker-compose -f $COMPOSE_FILE up -d --no-deps --scale backend=2 backend
    docker-compose -f $COMPOSE_FILE up -d --no-deps --scale frontend=2 frontend

    # Wait for new instances to be healthy
    sleep 30
    health_check "http://localhost:8000/health" "Backend (Green)"
    health_check "http://localhost:3000/" "Frontend (Green)"

    # Switch traffic to green deployment
    echo "🔄 Switching traffic to green deployment..."
    docker-compose -f $COMPOSE_FILE up -d nginx

    # Wait and verify
    sleep 10
    health_check "http://localhost/health" "Load Balancer"
    health_check "http://localhost/api/v1/foods" "API Endpoint"

    # Remove blue deployment
    echo "🔵 Removing blue deployment..."
    docker-compose -f $COMPOSE_FILE up -d --scale backend=1 --scale frontend=1

    echo "✅ Blue-green deployment completed"
}

# Standard deployment
standard_deploy() {
    echo "🚀 Starting standard deployment..."

    COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

    # Stop services gracefully
    echo "⏹️ Stopping services..."
    docker-compose -f $COMPOSE_FILE down --timeout 30

    # Start services
    echo "▶️ Starting services..."
    docker-compose -f $COMPOSE_FILE up -d

    # Wait for services to start
    echo "⏳ Waiting for services to start..."
    sleep 60

    # Health checks
    health_check "http://localhost/health" "Backend"
    health_check "http://localhost/" "Frontend"
    health_check "http://localhost/api/v1/foods" "API"

    echo "✅ Standard deployment completed"
}

# Post-deployment tests
run_post_deployment_tests() {
    echo "🧪 Running post-deployment tests..."

    # API tests
    echo "Testing API endpoints..."
    if ! curl -f "http://localhost/api/v1/foods" &> /dev/null; then
        echo "❌ API test failed"
        exit 1
    fi

    # Frontend test
    echo "Testing frontend..."
    if ! curl -f "http://localhost/" &> /dev/null; then
        echo "❌ Frontend test failed"
        exit 1
    fi

    echo "✅ Post-deployment tests passed"
}

# Cleanup old images
cleanup() {
    echo "🧹 Cleaning up old Docker images..."

    docker image prune -f
    docker volume prune -f

    # Keep only last 5 backups
    find backups -maxdepth 1 -type d | sort -r | tail -n +6 | xargs rm -rf

    echo "✅ Cleanup completed"
}

# Rollback function
rollback() {
    echo "🔄 Rolling back deployment..."

    COMPOSE_FILE="docker-compose.${ENVIRONMENT}.yml"

    # Get previous version from Git
    PREVIOUS_VERSION=$(git log --oneline -2 | tail -1 | cut -d' ' -f1)

    echo "Rolling back to version: $PREVIOUS_VERSION"
    git checkout $PREVIOUS_VERSION

    # Redeploy previous version
    docker-compose -f $COMPOSE_FILE down
    docker-compose -f $COMPOSE_FILE up -d

    # Restore database if needed
    if [ -f "backups/latest/database.sql" ]; then
        echo "Restoring database..."
        cat backups/latest/database.sql | docker exec -i ${PROJECT_NAME}-postgres psql -U $POSTGRES_USER -d $POSTGRES_DB
    fi

    echo "✅ Rollback completed"
}

# Main deployment process
main() {
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            load_environment
            validate_environment
            create_backup
            pull_images

            if [ "$ENVIRONMENT" = "production" ]; then
                blue_green_deploy
            else
                standard_deploy
            fi

            run_post_deployment_tests
            cleanup

            echo "=============================================="
            echo "🎉 Deployment completed successfully!"
            echo "Environment: $ENVIRONMENT"
            echo "Version: $VERSION"
            echo "Frontend: http://localhost"
            echo "API: http://localhost/api"
            echo "Monitoring: http://localhost:5000"
            echo "=============================================="
            ;;
        "rollback")
            rollback
            ;;
        "health")
            health_check "http://localhost/health" "Backend"
            health_check "http://localhost/" "Frontend"
            ;;
        *)
            echo "Usage: $0 {deploy|rollback|health} [environment] [version]"
            exit 1
            ;;
    esac
}

# Error handling
trap 'echo "❌ Deployment failed! Check logs for details."; exit 1' ERR

# Run main function
main "$@"