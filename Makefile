# Nutrition Intelligence Platform - Development Makefile

.PHONY: help up down build logs shell migrate seed test lint clean install

# Default environment
ENV ?= development
COMPOSE_FILE = infra/docker/docker-compose.yml

help: ## Show this help message
	@echo "Nutrition Intelligence Platform - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies for local development
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Dependencies installed successfully!"

up: ## Start all services
	@echo "Starting Nutrition Intelligence Platform..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "Services started! Access:"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Backend API: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/docs"
	@echo "  - PgAdmin: http://localhost:5050"
	@echo "  - MinIO Console: http://localhost:9001"

down: ## Stop all services
	@echo "Stopping services..."
	docker-compose -f $(COMPOSE_FILE) down

build: ## Build all Docker images
	@echo "Building Docker images..."
	docker-compose -f $(COMPOSE_FILE) build --no-cache

rebuild: down build up ## Rebuild and restart all services

logs: ## Show logs from all services
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## Show backend logs
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Show frontend logs  
	docker-compose -f $(COMPOSE_FILE) logs -f frontend

shell-backend: ## Open shell in backend container
	docker-compose -f $(COMPOSE_FILE) exec backend bash

shell-db: ## Open PostgreSQL shell
	docker-compose -f $(COMPOSE_FILE) exec postgres psql -U postgres -d nutrition_intelligence

migrate: ## Run database migrations
	@echo "Running database migrations..."
	docker-compose -f $(COMPOSE_FILE) exec backend alembic upgrade head
	@echo "Migrations completed!"

migrate-create: ## Create new migration (usage: make migrate-create MESSAGE="your message")
	@if [ -z "$(MESSAGE)" ]; then echo "Usage: make migrate-create MESSAGE=\"your message\""; exit 1; fi
	docker-compose -f $(COMPOSE_FILE) exec backend alembic revision --autogenerate -m "$(MESSAGE)"

migrate-rollback: ## Rollback last migration
	docker-compose -f $(COMPOSE_FILE) exec backend alembic downgrade -1

seed: ## Seed database with initial data
	@echo "Seeding database with initial data..."
	docker-compose -f $(COMPOSE_FILE) exec backend python -m scripts.seed_database
	@echo "Database seeded successfully!"

test: ## Run all tests
	@echo "Running backend tests..."
	docker-compose -f $(COMPOSE_FILE) exec backend pytest tests/ -v
	@echo "Running frontend tests..."
	docker-compose -f $(COMPOSE_FILE) exec frontend npm test

test-backend: ## Run backend tests only
	docker-compose -f $(COMPOSE_FILE) exec backend pytest tests/ -v

test-frontend: ## Run frontend tests only
	docker-compose -f $(COMPOSE_FILE) exec frontend npm test

lint: ## Run code linting
	@echo "Linting backend code..."
	docker-compose -f $(COMPOSE_FILE) exec backend black . --check
	docker-compose -f $(COMPOSE_FILE) exec backend ruff check .
	@echo "Linting frontend code..."
	docker-compose -f $(COMPOSE_FILE) exec frontend npm run lint

lint-fix: ## Fix linting issues
	@echo "Fixing backend linting issues..."
	docker-compose -f $(COMPOSE_FILE) exec backend black .
	docker-compose -f $(COMPOSE_FILE) exec backend ruff check . --fix
	@echo "Fixing frontend linting issues..."
	docker-compose -f $(COMPOSE_FILE) exec frontend npm run lint:fix

clean: ## Clean up containers, volumes, and images
	@echo "Cleaning up Docker resources..."
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker system prune -f
	@echo "Cleanup completed!"

backup-db: ## Backup database
	@echo "Creating database backup..."
	mkdir -p backups
	docker-compose -f $(COMPOSE_FILE) exec postgres pg_dump -U postgres nutrition_intelligence > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backup created in backups/ directory"

restore-db: ## Restore database from backup (usage: make restore-db FILE=backup_file.sql)
	@if [ -z "$(FILE)" ]; then echo "Usage: make restore-db FILE=backup_file.sql"; exit 1; fi
	@echo "Restoring database from $(FILE)..."
	docker-compose -f $(COMPOSE_FILE) exec -T postgres psql -U postgres nutrition_intelligence < $(FILE)
	@echo "Database restored successfully!"

status: ## Show service status
	docker-compose -f $(COMPOSE_FILE) ps

health: ## Check service health
	@echo "Checking service health..."
	@curl -s http://localhost:8000/health || echo "Backend: DOWN"
	@curl -s http://localhost:3000 > /dev/null && echo "Frontend: UP" || echo "Frontend: DOWN"

dev-backend: ## Run backend in development mode (outside Docker)
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run frontend in development mode (outside Docker)  
	cd frontend && npm start

setup: install build up migrate seed ## Complete setup for new developers

reset: down clean setup ## Reset entire environment

# Production commands
prod-build: ## Build production images
	ENV=production docker-compose -f $(COMPOSE_FILE) -f infra/docker/docker-compose.prod.yml build

prod-up: ## Start production services
	ENV=production docker-compose -f $(COMPOSE_FILE) -f infra/docker/docker-compose.prod.yml up -d

prod-down: ## Stop production services
	ENV=production docker-compose -f $(COMPOSE_FILE) -f infra/docker/docker-compose.prod.yml down