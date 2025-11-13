# Deployment Guide - Nutrition Intelligence

## Table of Contents

- [Overview](#overview)
- [Infrastructure](#infrastructure)
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Database Setup](#database-setup)
- [SSL/HTTPS Configuration](#sslhttps-configuration)
- [Monitoring Setup](#monitoring-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Overview

This guide covers deploying the Nutrition Intelligence platform to production using Docker, Google Cloud Platform (GCP), and Traefik for reverse proxy with automatic SSL.

**Current Production Environment:**
- **Server**: Google Cloud Platform e2-standard-2
- **Specs**: 2 vCPU, 8GB RAM, 50GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Location**: us-central1-c
- **URL**: https://nutrition-intelligence.scram2k.com
- **SSL**: Let's Encrypt via Traefik
- **Uptime**: 99.9%

## Infrastructure

### Architecture Overview

```
┌──────────────────────────────────────────┐
│        Internet (HTTPS Traffic)          │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│           Traefik Reverse Proxy             │
│  • Port 80 → 443 redirect                   │
│  • SSL/TLS termination (Let's Encrypt)      │
│  • Load balancing                           │
│  • Request routing                          │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌──────────┐ ┌────────────┐
│Frontend │ │ Backend  │ │ Monitoring │
│ (Nginx) │ │(FastAPI) │ │(Prometheus)│
│ :3005   │ │  :8000   │ │   :9090    │
└─────────┘ └────┬─────┘ └────────────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
┌───────────┐ ┌──────┐ ┌────────┐
│PostgreSQL │ │Redis │ │  Loki  │
│  :5432    │ │:6379 │ │ :3100  │
└───────────┘ └──────┘ └────────┘
```

### Services

| Service | Port | Purpose |
|---------|------|---------|
| Traefik | 80, 443 | Reverse proxy, SSL termination |
| Frontend | 3005 | React application |
| Backend | 8000 | FastAPI application |
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Cache and sessions |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Metrics visualization |
| Loki | 3100 | Log aggregation |
| Promtail | 9080 | Log collection |

## Prerequisites

### For Production Deployment

1. **Server Requirements**:
   - Ubuntu 22.04 LTS or later
   - Minimum 2 vCPU, 4GB RAM (recommended: 2 vCPU, 8GB RAM)
   - 50GB storage
   - Static public IP address

2. **Domain Configuration**:
   - Domain name registered
   - DNS A record pointing to server IP
   - DNS propagation completed

3. **Software**:
   - Docker Engine 24.0+
   - Docker Compose 2.20+
   - Git
   - gcloud CLI (for GCP)

4. **API Keys**:
   - Google Gemini API key
   - Anthropic Claude API key (optional)

5. **Access**:
   - SSH access to server
   - Sudo privileges
   - Firewall rules configured (ports 80, 443, 22)

## Local Development

### Quick Start with Docker Compose

```bash
# 1. Clone repository
git clone <repository-url>
cd "Nutrition Intelligence"

# 2. Configure environment
cp .env.example .env
# Edit .env with your configuration

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# 6. Stop services
docker-compose down
```

### Development Without Docker

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and Redis
docker-compose up -d db redis

# Configure environment
cp .env.example .env
# Edit .env

# Run migrations
python scripts/create_rag_tables.py

# Populate initial data
docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence < scripts/populate_rag_direct.sql

# Start backend
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm start
```

Access:
- Frontend: http://localhost:3005
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### Initial Server Setup

#### 1. Create GCP Instance

```bash
# Create e2-standard-2 instance
gcloud compute instances create nutrition-intelligence-prod \
  --project=mi-infraestructura-web \
  --zone=us-central1-c \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-ssd \
  --tags=http-server,https-server

# Reserve static IP
gcloud compute addresses create nutrition-intelligence-ip \
  --region=us-central1

# Attach static IP
gcloud compute instances add-access-config nutrition-intelligence-prod \
  --zone=us-central1-c \
  --address=$(gcloud compute addresses describe nutrition-intelligence-ip --region=us-central1 --format="value(address)")
```

#### 2. Configure Firewall Rules

```bash
# Allow HTTP
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags=http-server

# Allow HTTPS
gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --target-tags=https-server

# Allow SSH (if not already configured)
gcloud compute firewall-rules create allow-ssh \
  --allow tcp:22 \
  --target-tags=ssh-server
```

#### 3. Connect to Server

```bash
# SSH into server
gcloud compute ssh nutrition-intelligence-prod \
  --zone=us-central1-c \
  --project=mi-infraestructura-web
```

#### 4. Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version

# Logout and login again for group changes
exit
```

#### 5. Clone Repository

```bash
# Create application directory
sudo mkdir -p /srv/scram/nutrition-intelligence
sudo chown $USER:$USER /srv/scram/nutrition-intelligence

# Clone repository
cd /srv/scram
git clone <repository-url> nutrition-intelligence
cd nutrition-intelligence
```

### Configure Production Environment

#### 1. Create Production .env File

```bash
cd /srv/scram/nutrition-intelligence

# Create .env file
cat > .env << 'EOF'
# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DATABASE_URL=postgresql://nutrition_user:CHANGE_THIS_PASSWORD@db:5432/nutrition_intelligence
POSTGRES_USER=nutrition_user
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD
POSTGRES_DB=nutrition_intelligence

# ============================================================================
# REDIS CONFIGURATION
# ============================================================================
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=50
REDIS_TIMEOUT=5

# ============================================================================
# AI CONFIGURATION
# ============================================================================
GOOGLE_API_KEY=your-google-gemini-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
AI_VISION_MODEL=gemini
AI_VISION_CONFIDENCE_THRESHOLD=75
RAG_MODEL=gemini-1.5-flash-latest
RAG_MAX_CONTEXT_LENGTH=5000
RAG_TEMPERATURE=0.7

# ============================================================================
# SECURITY
# ============================================================================
SECRET_KEY=CHANGE_THIS_TO_RANDOM_STRING_MIN_32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================================================
# APPLICATION
# ============================================================================
APP_ENV=production
DEBUG=false
ALLOWED_ORIGINS=https://nutrition-intelligence.scram2k.com

# ============================================================================
# TRAEFIK
# ============================================================================
DOMAIN=nutrition-intelligence.scram2k.com
EMAIL=admin@scram2k.com

# ============================================================================
# MONITORING
# ============================================================================
PROMETHEUS_RETENTION=15d
GRAFANA_ADMIN_PASSWORD=CHANGE_THIS_PASSWORD
EOF

# Secure .env file
chmod 600 .env

# Copy to backend directory
cp .env backend/.env
```

**Important**: Replace all `CHANGE_THIS_*` values with secure passwords and real API keys.

#### 2. Generate Secure Secrets

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate database password
openssl rand -base64 32

# Generate Grafana password
openssl rand -base64 16
```

### Deploy to Production

#### 1. Build and Start Services

```bash
cd /srv/scram/nutrition-intelligence

# Pull latest code
git pull origin main

# Build and start all services
docker compose up -d --build

# Check status
docker compose ps

# View logs
docker compose logs -f
```

#### 2. Initialize Database

```bash
# Create RAG tables
docker exec nutrition-intelligence-backend python scripts/create_rag_tables.py

# Populate initial data
docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence < backend/scripts/populate_rag_direct.sql

# Run database optimizations
docker cp backend/scripts/optimize_database.sql nutrition-intelligence-db:/tmp/
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -f /tmp/optimize_database.sql
```

#### 3. Verify Deployment

```bash
# Run health check
./backend/scripts/health_check.sh

# Check individual services
curl http://localhost:8000/health
curl http://localhost:3005/health
curl http://localhost:8000/api/v1/rag/health

# Test from outside
curl https://nutrition-intelligence.scram2k.com/health
```

## Database Setup

### PostgreSQL Configuration

#### Production Database Settings

```bash
# Connect to database container
docker exec -it nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence

# Apply performance settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET max_connections = 100;

# Restart PostgreSQL for changes
docker compose restart db
```

#### Backup Configuration

```bash
# Create backup directory
sudo mkdir -p /srv/backups/nutrition-intelligence
sudo chown $USER:$USER /srv/backups/nutrition-intelligence

# Manual backup
docker exec nutrition-intelligence-db pg_dump -U nutrition_user nutrition_intelligence > /srv/backups/nutrition-intelligence/backup_$(date +%Y%m%d_%H%M%S).sql

# Automated daily backups (cron)
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * docker exec nutrition-intelligence-db pg_dump -U nutrition_user nutrition_intelligence > /srv/backups/nutrition-intelligence/backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql

# Backup retention script (keep last 30 days)
0 3 * * * find /srv/backups/nutrition-intelligence -name "backup_*.sql" -mtime +30 -delete
```

#### Restore from Backup

```bash
# Stop application
docker compose stop backend

# Restore database
docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence < /srv/backups/nutrition-intelligence/backup_20251111_020000.sql

# Start application
docker compose start backend
```

## SSL/HTTPS Configuration

### Traefik with Let's Encrypt

The deployment uses Traefik for automatic SSL certificate management with Let's Encrypt.

#### Traefik Configuration

`docker-compose.prod.yml` includes:

```yaml
traefik:
  image: traefik:v2.10
  command:
    - "--providers.docker=true"
    - "--entrypoints.web.address=:80"
    - "--entrypoints.websecure.address=:443"
    - "--certificatesresolvers.letsencrypt.acme.email=${EMAIL}"
    - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - ./letsencrypt:/letsencrypt
```

#### Service Labels for SSL

```yaml
frontend:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
    - "traefik.http.routers.frontend.entrypoints=websecure"
    - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
```

#### Certificate Renewal

- Certificates auto-renew 30 days before expiration
- Stored in `./letsencrypt/acme.json`
- Backup this file for certificate portability

```bash
# Backup SSL certificates
sudo cp /srv/scram/nutrition-intelligence/letsencrypt/acme.json /srv/backups/nutrition-intelligence/acme.json.backup
```

#### Force Certificate Regeneration

```bash
# Stop Traefik
docker compose stop traefik

# Remove old certificate
sudo rm /srv/scram/nutrition-intelligence/letsencrypt/acme.json

# Start Traefik (new certificate will be issued)
docker compose up -d traefik

# Check logs
docker compose logs -f traefik
```

## Monitoring Setup

### Prometheus Configuration

```bash
# Prometheus config already at infra/monitoring/prometheus-nutrition.yml
# Verify it's loaded
docker compose logs prometheus | grep "configuration"
```

### Grafana Setup

1. **Access Grafana**: https://nutrition-intelligence.scram2k.com:3000
2. **Login**: admin / (password from .env)
3. **Add Prometheus Data Source**:
   - URL: http://prometheus:9090
   - Save & Test

4. **Import Dashboard**:
   - Upload `infra/monitoring/grafana-dashboard.json`
   - Select Prometheus data source

### Loki and Promtail

Logs are automatically collected from all Docker containers.

**View logs in Grafana**:
- Go to Explore
- Select Loki data source
- Query: `{container_name="nutrition-intelligence-backend"}`

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /srv/scram/nutrition-intelligence
            git pull origin main
            docker compose down
            docker compose up -d --build
            docker compose ps
```

### Secrets to Configure

In GitHub repository settings, add:
- `SERVER_HOST`: Server IP or domain
- `SERVER_USER`: SSH username
- `SSH_PRIVATE_KEY`: Private SSH key

### Manual Deployment

```bash
# On local machine
git push origin main

# SSH to production server
gcloud compute ssh prod-server --zone=us-central1-c --project=mi-infraestructura-web

# Pull and deploy
cd /srv/scram/nutrition-intelligence
git pull origin main
docker compose down
docker compose up -d --build

# Verify
./backend/scripts/health_check.sh
```

## Maintenance

### Update Dependencies

#### Backend

```bash
cd /srv/scram/nutrition-intelligence/backend

# Update requirements
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Rebuild
docker compose up -d --build backend
```

#### Frontend

```bash
cd /srv/scram/nutrition-intelligence/frontend

# Update packages
npm update

# Rebuild
docker compose up -d --build frontend
```

### Database Maintenance

```bash
# VACUUM ANALYZE (reclaim space and update statistics)
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "VACUUM ANALYZE;"

# Reindex database
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "REINDEX DATABASE nutrition_intelligence;"

# Check database size
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "SELECT pg_size_pretty(pg_database_size('nutrition_intelligence'));"
```

### Redis Maintenance

```bash
# Clear all cache
docker exec nutrition-intelligence-redis redis-cli FLUSHDB

# Clear specific pattern
docker exec nutrition-intelligence-redis redis-cli --scan --pattern "user:*" | xargs docker exec -i nutrition-intelligence-redis redis-cli DEL

# View memory usage
docker exec nutrition-intelligence-redis redis-cli INFO memory
```

### Log Rotation

Logs are handled by Docker's logging driver. Configure in `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Then restart Docker:

```bash
sudo systemctl restart docker
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker compose logs backend
docker compose logs frontend
docker compose logs db

# Check resource usage
docker stats

# Restart specific service
docker compose restart backend

# Rebuild from scratch
docker compose down
docker compose up -d --build
```

### Database Connection Errors

```bash
# Check database is running
docker compose ps db

# Check database logs
docker compose logs db

# Test connection
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "SELECT 1;"

# Verify credentials in .env
cat .env | grep DATABASE_URL
```

### SSL Certificate Issues

```bash
# Check Traefik logs
docker compose logs traefik | grep -i error

# Verify domain DNS
dig nutrition-intelligence.scram2k.com

# Check certificate file
sudo cat /srv/scram/nutrition-intelligence/letsencrypt/acme.json

# Force regeneration (see SSL section above)
```

### High Memory Usage

```bash
# Check container memory
docker stats

# Restart heavy services
docker compose restart backend db

# Clear Redis cache
docker exec nutrition-intelligence-redis redis-cli FLUSHDB

# Check for memory leaks in logs
docker compose logs backend | grep -i memory
```

### Slow Performance

```bash
# Check database queries
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';"

# Check Redis stats
docker exec nutrition-intelligence-redis redis-cli INFO stats

# Verify indexes are being used
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -c "EXPLAIN ANALYZE SELECT * FROM productos_nom051 WHERE nombre ILIKE '%coca%';"

# Re-run optimizations
docker exec nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence -f /tmp/optimize_database.sql
```

### Disk Space Issues

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a
docker volume prune

# Clean old logs
sudo journalctl --vacuum-time=7d

# Clean old backups
find /srv/backups/nutrition-intelligence -name "backup_*.sql" -mtime +30 -delete
```

## Rollback Procedure

### Quick Rollback

```bash
cd /srv/scram/nutrition-intelligence

# Stop current version
docker compose down

# Checkout previous version
git log --oneline  # Find commit hash
git checkout <previous-commit-hash>

# Deploy
docker compose up -d --build

# If database changes, restore backup
docker exec -i nutrition-intelligence-db psql -U nutrition_user -d nutrition_intelligence < /srv/backups/nutrition-intelligence/backup_YYYYMMDD_HHMMSS.sql
```

## Security Checklist

- [ ] `.env` file permissions set to 600
- [ ] Strong passwords for all services
- [ ] Firewall configured (only 80, 443, 22 open)
- [ ] SSH key-based authentication
- [ ] SSL certificates valid and auto-renewing
- [ ] Database backups automated
- [ ] Rate limiting enabled
- [ ] Monitoring and alerts configured
- [ ] Logs being collected and rotated
- [ ] Dependencies up to date

## Production Checklist

Before going live:

- [ ] Domain configured with proper DNS
- [ ] SSL certificates issued and working
- [ ] All environment variables set correctly
- [ ] Database initialized and optimized
- [ ] Initial data populated
- [ ] All services healthy
- [ ] Monitoring dashboards configured
- [ ] Backup automation tested
- [ ] Load testing performed
- [ ] Documentation updated
- [ ] Rollback procedure tested

## Support

For deployment issues:
- **Documentation**: Check all docs in `docs/` folder
- **Logs**: Always check `docker compose logs`
- **Health Checks**: Run `./backend/scripts/health_check.sh`
- **Monitoring**: Check Grafana dashboards

---

**Last Updated**: 2025-11-11
**Deployment Version**: 1.0.0
**Production URL**: https://nutrition-intelligence.scram2k.com
