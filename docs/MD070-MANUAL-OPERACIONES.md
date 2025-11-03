# MD070 - Manual de Operaciones y Deployment

## Nutrition Intelligence Platform - Guía Operacional Completa

**Versión:** 1.0.0
**Fecha:** Enero 2025
**Autor:** Equipo de Arquitectura de Software
**Estado:** Producción

---

## 📋 Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación y Configuración](#3-instalación-y-configuración)
4. [Deployment](#4-deployment)
5. [Operación y Mantenimiento](#5-operación-y-mantenimiento)
6. [Monitoreo y Observabilidad](#6-monitoreo-y-observabilidad)
7. [Backup y Recuperación](#7-backup-y-recuperación)
8. [Seguridad Operacional](#8-seguridad-operacional)
9. [Troubleshooting](#9-troubleshooting)
10. [Procedimientos de Emergencia](#10-procedimientos-de-emergencia)
11. [Apéndices](#11-apéndices)

---

## 1. Introducción

### 1.1 Propósito del Documento

Este manual proporciona instrucciones completas para la instalación, configuración, deployment, operación y mantenimiento de **Nutrition Intelligence Platform**, un sistema profesional de gestión nutricional diseñado específicamente para el mercado mexicano.

### 1.2 Audiencia

- **DevOps Engineers** - Deployment y CI/CD
- **System Administrators** - Operación y mantenimiento
- **Database Administrators** - Gestión de datos
- **Security Engineers** - Configuración de seguridad
- **Technical Support** - Troubleshooting

### 1.3 Alcance del Sistema

Nutrition Intelligence es una plataforma web full-stack que incluye:

- **Frontend:** React 18.2 + Material-UI
- **Backend:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15+ / SQLite (desarrollo)
- **AI Services:** Google Gemini + Anthropic Claude
- **Messaging:** Twilio WhatsApp API
- **Monitoring:** Prometheus + Grafana + Loki

---

## 2. Requisitos del Sistema

### 2.1 Requisitos de Hardware

#### Servidor de Desarrollo
```
CPU:     4 cores (Intel i5 o superior)
RAM:     8 GB mínimo, 16 GB recomendado
Disco:   50 GB SSD
Red:     100 Mbps
```

#### Servidor de Producción
```
CPU:     8 cores (Intel Xeon o AMD EPYC)
RAM:     32 GB mínimo, 64 GB recomendado
Disco:   500 GB SSD NVMe (RAID 10)
Red:     1 Gbps
```

#### Base de Datos (Producción)
```
CPU:     8 cores
RAM:     64 GB (PostgreSQL cache)
Disco:   1 TB SSD (RAID 10)
IOPS:    10,000+ (para buen rendimiento)
```

### 2.2 Requisitos de Software

#### Sistema Operativo

**Desarrollo:**
- Windows 10/11 Pro
- macOS 12+ (Monterey)
- Linux (Ubuntu 20.04+, RHEL 8+)

**Producción:**
- Ubuntu Server 22.04 LTS (recomendado)
- RHEL 9 / Rocky Linux 9
- Debian 12

#### Runtime y Dependencias

**Backend:**
```bash
Python:      3.11+
pip:         23.0+
uvicorn:     0.25.0+
PostgreSQL:  15.0+
Redis:       7.0+ (opcional, para caché)
```

**Frontend:**
```bash
Node.js:     18.0+ LTS
npm:         9.0+
```

**Servicios Externos:**
```bash
Docker:      24.0+
Docker Compose: 2.20+
Git:         2.40+
```

### 2.3 Acceso a APIs Externas

```bash
# AI Vision Services
Google Gemini API:        https://ai.google.dev/
Anthropic Claude API:     https://console.anthropic.com/

# Messaging
Twilio WhatsApp API:      https://www.twilio.com/whatsapp

# Opcional
SendGrid (Email):         https://sendgrid.com/
Google Cloud Storage:     https://cloud.google.com/storage
```

---

## 3. Instalación y Configuración

### 3.1 Instalación en Desarrollo (Local)

#### 3.1.1 Clonar Repositorio

```bash
git clone https://github.com/nutrition-intelligence/platform.git
cd platform
```

#### 3.1.2 Configurar Backend

```bash
# Navegar a directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus credenciales
# Windows:
notepad .env
# Linux/Mac:
nano .env
```

**Configuración .env mínima:**
```bash
# Base de datos (SQLite para desarrollo)
DATABASE_URL=sqlite+aiosqlite:///./nutrition_intelligence.db

# Secret key (generar con: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=tu-secret-key-segura-aqui

# API Keys (opcional para desarrollo)
GOOGLE_API_KEY=tu-google-api-key
ANTHROPIC_API_KEY=tu-anthropic-api-key
TWILIO_ACCOUNT_SID=tu-twilio-sid
TWILIO_AUTH_TOKEN=tu-twilio-token

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3002,http://localhost:3005
```

#### 3.1.3 Inicializar Base de Datos

```bash
# Ejecutar migraciones (si existen)
# alembic upgrade head

# O inicializar base de datos con script
python scripts/init_db.py

# Poblar datos de ejemplo (SMAE, equivalentes)
python scripts/populate_smae_foods.py
```

#### 3.1.4 Iniciar Backend

```bash
# Modo desarrollo con auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Verificar que está corriendo
curl http://localhost:8000/docs
```

#### 3.1.5 Configurar Frontend

```bash
# Nueva terminal, navegar a frontend
cd frontend

# Instalar dependencias
npm install

# Configurar API endpoint
# Editar src/config/api.js si es necesario

# Iniciar desarrollo
npm start

# La app se abrirá en http://localhost:3002
```

### 3.2 Instalación con Docker (Recomendado)

#### 3.2.1 Docker Compose

Crear archivo `docker-compose.yml` en el root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: nutrition-db
    environment:
      POSTGRES_DB: nutrition_intelligence
      POSTGRES_USER: nutrition_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/scripts/init_db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nutrition_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: nutrition-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: nutrition-backend
    environment:
      DATABASE_URL: postgresql+asyncpg://nutrition_user:${DB_PASSWORD}@db:5432/nutrition_intelligence
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      TWILIO_ACCOUNT_SID: ${TWILIO_ACCOUNT_SID}
      TWILIO_AUTH_TOKEN: ${TWILIO_AUTH_TOKEN}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: nutrition-frontend
    ports:
      - "3002:80"
    depends_on:
      - backend
    environment:
      REACT_APP_API_URL: http://localhost:8000

  # Prometheus Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: nutrition-prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    ports:
      - "9090:9090"

  # Grafana Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: nutrition-grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  # Loki Log Aggregation
  loki:
    image: grafana/loki:latest
    container_name: nutrition-loki
    ports:
      - "3100:3100"
    volumes:
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
  loki_data:
```

#### 3.2.2 Iniciar con Docker

```bash
# Crear archivo .env con variables de entorno
cat > .env << EOF
DB_PASSWORD=secure_password_here
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
GOOGLE_API_KEY=your-google-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
GRAFANA_PASSWORD=admin_password
EOF

# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Verificar servicios
docker-compose ps
```

**URLs de Servicios:**
- Frontend: http://localhost:3002
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Loki: http://localhost:3100

---

## 4. Deployment

### 4.1 Deployment en Producción (Linux Server)

#### 4.1.1 Preparación del Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias base
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql-15 \
    redis-server \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar versiones
python3.11 --version
node --version
npm --version
psql --version
```

#### 4.1.2 Configurar PostgreSQL

```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear usuario y base de datos
CREATE USER nutrition_user WITH PASSWORD 'secure_password_here';
CREATE DATABASE nutrition_intelligence OWNER nutrition_user;
GRANT ALL PRIVILEGES ON DATABASE nutrition_intelligence TO nutrition_user;

# Habilitar extensiones necesarias
\c nutrition_intelligence
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\q

# Configurar acceso remoto (si es necesario)
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Agregar: host nutrition_intelligence nutrition_user 0.0.0.0/0 md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

#### 4.1.3 Desplegar Backend

```bash
# Crear usuario de sistema
sudo useradd -m -s /bin/bash nutrition
sudo su - nutrition

# Clonar repositorio
git clone https://github.com/nutrition-intelligence/platform.git
cd platform/backend

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Configurar .env producción
cp .env.example .env
nano .env
```

**Configuración .env Producción:**
```bash
ENVIRONMENT=production
DEBUG=false

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://nutrition_user:secure_password@localhost:5432/nutrition_intelligence

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=<generar-con-secrets.token_urlsafe>
ALLOWED_HOSTS=nutrition-intelligence.com,www.nutrition-intelligence.com
CORS_ORIGINS=https://nutrition-intelligence.com,https://www.nutrition-intelligence.com

# APIs
GOOGLE_API_KEY=production-google-api-key
ANTHROPIC_API_KEY=production-anthropic-api-key
TWILIO_ACCOUNT_SID=production-twilio-sid
TWILIO_AUTH_TOKEN=production-twilio-token
```

#### 4.1.4 Crear Servicio Systemd (Backend)

```bash
# Salir del usuario nutrition
exit

# Crear servicio
sudo nano /etc/systemd/system/nutrition-backend.service
```

```ini
[Unit]
Description=Nutrition Intelligence Backend API
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=nutrition
Group=nutrition
WorkingDirectory=/home/nutrition/platform/backend
Environment="PATH=/home/nutrition/platform/backend/venv/bin"
EnvironmentFile=/home/nutrition/platform/backend/.env

ExecStart=/home/nutrition/platform/backend/venv/bin/gunicorn \
    main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/nutrition/access.log \
    --error-logfile /var/log/nutrition/error.log \
    --log-level info

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

```bash
# Crear directorio de logs
sudo mkdir -p /var/log/nutrition
sudo chown nutrition:nutrition /var/log/nutrition

# Habilitar e iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable nutrition-backend
sudo systemctl start nutrition-backend

# Verificar estado
sudo systemctl status nutrition-backend
```

#### 4.1.5 Desplegar Frontend

```bash
sudo su - nutrition
cd /home/nutrition/platform/frontend

# Instalar dependencias
npm install

# Configurar API URL para producción
nano src/config/api.js
# export const API_BASE_URL = 'https://api.nutrition-intelligence.com';

# Build para producción
npm run build

# Los archivos estáticos estarán en: build/
```

#### 4.1.6 Configurar Nginx

```bash
exit  # Salir de usuario nutrition

# Crear configuración Nginx
sudo nano /etc/nginx/sites-available/nutrition-intelligence
```

```nginx
# Backend API
upstream backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

# Frontend (www y apex)
server {
    listen 80;
    listen [::]:80;
    server_name nutrition-intelligence.com www.nutrition-intelligence.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name nutrition-intelligence.com www.nutrition-intelligence.com;

    # SSL Certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/nutrition-intelligence.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nutrition-intelligence.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Root directory
    root /home/nutrition/platform/frontend/build;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

    # Frontend static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}

# Backend API subdomain
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.nutrition-intelligence.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/nutrition-intelligence.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nutrition-intelligence.com/privkey.pem;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy to backend
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_buffering off;
        proxy_read_timeout 120s;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/nutrition-intelligence /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Obtener certificados SSL
sudo certbot --nginx -d nutrition-intelligence.com -d www.nutrition-intelligence.com -d api.nutrition-intelligence.com

# Reiniciar Nginx
sudo systemctl restart nginx

# Habilitar auto-renovación de certificados
sudo systemctl enable certbot.timer
```

### 4.2 Deployment con CI/CD (GitHub Actions)

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run tests
        run: |
          cd backend
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.PROD_SERVER_HOST }}
          username: ${{ secrets.PROD_SERVER_USER }}
          key: ${{ secrets.PROD_SERVER_SSH_KEY }}
          script: |
            cd /home/nutrition/platform
            git pull origin main

            # Backend
            cd backend
            source venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart nutrition-backend

            # Frontend
            cd ../frontend
            npm install
            npm run build
            sudo systemctl reload nginx

            echo "✅ Deployment completed successfully"
```

---

## 5. Operación y Mantenimiento

### 5.1 Operaciones Diarias

#### 5.1.1 Monitoreo de Servicios

```bash
# Verificar estado de servicios
sudo systemctl status nutrition-backend
sudo systemctl status postgresql
sudo systemctl status redis
sudo systemctl status nginx

# Ver logs en tiempo real
sudo journalctl -u nutrition-backend -f
sudo tail -f /var/log/nutrition/error.log
sudo tail -f /var/log/nginx/error.log
```

#### 5.1.2 Verificación de Salud del Sistema

```bash
# CPU y Memoria
htop
free -h

# Espacio en disco
df -h

# Conexiones de red
sudo netstat -tulpn | grep -E '(8000|80|443|5432|6379)'

# Procesos del backend
ps aux | grep gunicorn

# Conexiones a PostgreSQL
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='nutrition_intelligence';"
```

### 5.2 Tareas de Mantenimiento

#### 5.2.1 Actualización de Dependencias

```bash
# Backend
cd /home/nutrition/platform/backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <package_name>
pip freeze > requirements.txt

# Frontend
cd /home/nutrition/platform/frontend
npm outdated
npm update
```

#### 5.2.2 Limpieza de Logs

```bash
# Configurar rotación de logs
sudo nano /etc/logrotate.d/nutrition
```

```
/var/log/nutrition/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 nutrition nutrition
    sharedscripts
    postrotate
        systemctl reload nutrition-backend > /dev/null
    endscript
}
```

#### 5.2.3 Optimización de Base de Datos

```bash
# Conectar a PostgreSQL
sudo -u postgres psql -d nutrition_intelligence

-- Vacuum completo
VACUUM FULL ANALYZE;

-- Reindex tablas principales
REINDEX DATABASE nutrition_intelligence;

-- Analizar estadísticas
ANALYZE VERBOSE;

-- Ver tamaño de tablas
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

\q
```

---

## 6. Monitoreo y Observabilidad

### 6.1 Prometheus Metrics

**Configuración:** `monitoring/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Backend API
  - job_name: 'nutrition-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'

  # PostgreSQL
  - job_name: 'postgresql'
    static_configs:
      - targets: ['localhost:9187']

  # Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']

  # Node Exporter (sistema)
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  # Nginx
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
```

### 6.2 Grafana Dashboards

Importar dashboards predefinidos:
- **ID 1860:** Node Exporter Full
- **ID 9628:** PostgreSQL Database
- **ID 11835:** Redis Dashboard
- **ID 12223:** Nginx Dashboard

**Dashboard Personalizado: Nutrition Intelligence**

Métricas clave:
- Request rate (requests/sec)
- Response time (p50, p95, p99)
- Error rate (%)
- Active users
- AI API calls (Gemini/Claude)
- WhatsApp messages sent
- Database connections
- Cache hit rate

### 6.3 Alertas

Configurar alertas en Prometheus Alertmanager:

```yaml
# monitoring/alerts.yml
groups:
  - name: nutrition_intelligence
    interval: 30s
    rules:
      # Alta tasa de errores
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Alta tasa de errores (> 5%)"

      # API lenta
      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API respondiendo lento (p95 > 2s)"

      # Base de datos saturada
      - alert: DatabaseConnectionPoolExhausted
        expr: pg_stat_database_numbackends{datname="nutrition_intelligence"} > 80
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Pool de conexiones agotado"

      # Disco casi lleno
      - alert: DiskSpaceWarning
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Espacio en disco bajo (< 15%)"
```

---

## 7. Backup y Recuperación

### 7.1 Backup de PostgreSQL

#### 7.1.1 Backup Diario Automatizado

```bash
#!/bin/bash
# /home/nutrition/scripts/backup-db.sh

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="nutrition_intelligence"
DB_USER="nutrition_user"

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup completo
pg_dump -U $DB_USER -F c -b -v -f "$BACKUP_DIR/${DB_NAME}_${DATE}.backup" $DB_NAME

# Backup SQL plano (para inspección)
pg_dump -U $DB_USER -F p -f "$BACKUP_DIR/${DB_NAME}_${DATE}.sql" $DB_NAME

# Comprimir backup SQL
gzip "$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# Eliminar backups antiguos (> 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "✅ Backup completado: ${DB_NAME}_${DATE}.backup"
```

```bash
# Dar permisos de ejecución
chmod +x /home/nutrition/scripts/backup-db.sh

# Agregar a crontab
crontab -e
# Agregar: 0 2 * * * /home/nutrition/scripts/backup-db.sh >> /var/log/nutrition/backup.log 2>&1
```

#### 7.1.2 Restaurar Backup

```bash
# Detener backend
sudo systemctl stop nutrition-backend

# Restaurar desde backup
pg_restore -U nutrition_user -d nutrition_intelligence -v /backup/postgresql/nutrition_intelligence_20250115_020000.backup

# O desde SQL
gunzip < /backup/postgresql/nutrition_intelligence_20250115_020000.sql.gz | psql -U nutrition_user -d nutrition_intelligence

# Reiniciar backend
sudo systemctl start nutrition-backend
```

### 7.2 Backup de Archivos Estáticos

```bash
#!/bin/bash
# /home/nutrition/scripts/backup-files.sh

BACKUP_DIR="/backup/files"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup de uploads (fotos de pacientes, archivos clínicos)
tar -czf "$BACKUP_DIR/uploads_${DATE}.tar.gz" /home/nutrition/platform/backend/uploads

# Backup de configuración
tar -czf "$BACKUP_DIR/config_${DATE}.tar.gz" /home/nutrition/platform/backend/.env /etc/nginx/sites-available/nutrition-intelligence

# Eliminar backups antiguos
find $BACKUP_DIR -type f -mtime +60 -delete

echo "✅ Backup de archivos completado"
```

### 7.3 Backup Offsite

```bash
# Sincronizar a almacenamiento remoto (S3/GCS)
aws s3 sync /backup/ s3://nutrition-intelligence-backups/ --delete

# O usar rclone para múltiples proveedores
rclone sync /backup/ remote:nutrition-intelligence-backups
```

---

## 8. Seguridad Operacional

### 8.1 Hardening del Sistema

```bash
# Firewall (UFW)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Fail2Ban (protección brute-force)
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configurar jail SSH
sudo nano /etc/fail2ban/jail.local
```

```ini
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

### 8.2 Auditoría y Cumplimiento

```bash
# Logs de auditoría (NOM-004-SSA3-2012)
# Los logs se almacenan automáticamente en:
# - /var/log/nutrition/audit.log (acciones de usuarios)
# - /var/log/nutrition/access.log (accesos HTTP)
# - PostgreSQL logs (cambios en datos de pacientes)

# Retención: 7 años (2555 días) según normativa mexicana
```

### 8.3 Rotación de Secrets

```bash
# Generar nuevo SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Actualizar .env
nano /home/nutrition/platform/backend/.env

# Reiniciar servicio
sudo systemctl restart nutrition-backend

# Invalidar sesiones antiguas en Redis
redis-cli FLUSHDB
```

---

## 9. Troubleshooting

### 9.1 Backend no inicia

**Síntoma:** El servicio `nutrition-backend` falla al iniciar

**Diagnóstico:**
```bash
# Ver logs del servicio
sudo journalctl -u nutrition-backend -n 50 --no-pager

# Ver logs de aplicación
sudo tail -n 100 /var/log/nutrition/error.log

# Verificar Python
sudo -u nutrition /home/nutrition/platform/backend/venv/bin/python --version

# Verificar dependencias
sudo -u nutrition /home/nutrition/platform/backend/venv/bin/pip check
```

**Soluciones:**
```bash
# Reinstalar dependencias
sudo -u nutrition bash -c "cd /home/nutrition/platform/backend && source venv/bin/activate && pip install -r requirements.txt"

# Verificar permisos
sudo chown -R nutrition:nutrition /home/nutrition/platform

# Verificar .env
sudo -u nutrition cat /home/nutrition/platform/backend/.env | grep DATABASE_URL

# Probar arranque manual
sudo -u nutrition bash -c "cd /home/nutrition/platform/backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"
```

### 9.2 Base de Datos lenta

**Síntoma:** Queries lentas, timeouts

**Diagnóstico:**
```sql
-- Conectar a PostgreSQL
sudo -u postgres psql -d nutrition_intelligence

-- Ver queries lentas
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state != 'idle'
  AND now() - query_start > interval '5 seconds'
ORDER BY duration DESC;

-- Ver índices faltantes
SELECT schemaname, tablename, attname, n_distinct
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100
ORDER BY n_distinct DESC;

-- Ver bloqueos
SELECT * FROM pg_locks WHERE NOT granted;
```

**Soluciones:**
```sql
-- Terminar queries bloqueadas
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND now() - state_change > interval '10 minutes';

-- VACUUM y ANALYZE
VACUUM ANALYZE;

-- Crear índices faltantes (ejemplo)
CREATE INDEX idx_patients_email ON patients(email);
CREATE INDEX idx_laboratory_data_patient_id ON laboratory_data(patient_id);
```

### 9.3 Error 502 Bad Gateway

**Síntoma:** Nginx retorna 502

**Diagnóstico:**
```bash
# Verificar backend
sudo systemctl status nutrition-backend

# Ver logs Nginx
sudo tail -f /var/log/nginx/error.log

# Probar conexión backend
curl http://localhost:8000/docs
```

**Soluciones:**
```bash
# Reiniciar backend
sudo systemctl restart nutrition-backend

# Reiniciar Nginx
sudo systemctl restart nginx

# Verificar firewall
sudo ufw status

# Aumentar timeouts en Nginx
sudo nano /etc/nginx/sites-available/nutrition-intelligence
# proxy_read_timeout 300;
# proxy_connect_timeout 300;
```

### 9.4 Memoria Agotada

**Síntoma:** OOM Killer termina procesos

**Diagnóstico:**
```bash
# Ver memoria
free -h

# Ver procesos por memoria
ps aux --sort=-%mem | head -20

# Ver logs del kernel
dmesg | grep -i 'out of memory'
```

**Soluciones:**
```bash
# Reducir workers de Gunicorn
sudo nano /etc/systemd/system/nutrition-backend.service
# Cambiar --workers a 2

# Configurar swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Agregar a /etc/fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimizar PostgreSQL
sudo nano /etc/postgresql/15/main/postgresql.conf
# shared_buffers = 2GB
# effective_cache_size = 6GB
# work_mem = 16MB
```

---

## 10. Procedimientos de Emergencia

### 10.1 Servicio Caído - Restauración Rápida

```bash
#!/bin/bash
# emergency-restore.sh

echo "🚨 RESTAURACIÓN DE EMERGENCIA"

# 1. Reiniciar todos los servicios
sudo systemctl restart postgresql
sudo systemctl restart redis
sudo systemctl restart nutrition-backend
sudo systemctl restart nginx

# 2. Verificar estado
sleep 5
systemctl is-active postgresql redis nutrition-backend nginx

# 3. Test de conectividad
curl -f http://localhost:8000/health || echo "❌ Backend no responde"
curl -f http://localhost/ || echo "❌ Frontend no responde"

echo "✅ Restauración completada"
```

### 10.2 Corrupción de Datos

```bash
# 1. Detener escrituras
sudo systemctl stop nutrition-backend

# 2. Backup de emergencia
pg_dump -U nutrition_user -F c -f /tmp/emergency_backup_$(date +%s).backup nutrition_intelligence

# 3. Verificar integridad
sudo -u postgres pg_dump -U nutrition_user nutrition_intelligence | psql -U nutrition_user -d nutrition_intelligence_test

# 4. Si está OK, restaurar desde backup más reciente
pg_restore -U nutrition_user -d nutrition_intelligence -c /backup/postgresql/latest.backup

# 5. Reiniciar servicio
sudo systemctl start nutrition-backend
```

### 10.3 Ataque de Seguridad Detectado

```bash
# 1. Aislar servidor
sudo ufw default deny incoming

# 2. Preservar evidencia
sudo tar -czf /tmp/forensics_$(date +%s).tar.gz \
    /var/log/nginx/ \
    /var/log/nutrition/ \
    /var/log/auth.log \
    /var/log/syslog

# 3. Revisar conexiones activas
sudo netstat -tulpn
sudo ss -s

# 4. Bloquear IPs sospechosas
sudo fail2ban-client set sshd banip <IP_ADDRESS>

# 5. Rotar secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Actualizar .env con nuevo SECRET_KEY

# 6. Forzar logout de todos los usuarios
redis-cli FLUSHDB

# 7. Reiniciar con nuevo secret
sudo systemctl restart nutrition-backend

# 8. Notificar al equipo de seguridad
```

---

## 11. Apéndices

### 11.1 Checklist de Deployment

- [ ] Servidor preparado (OS actualizado, dependencias instaladas)
- [ ] PostgreSQL configurado y optimizado
- [ ] Redis instalado y corriendo
- [ ] Usuario `nutrition` creado
- [ ] Repositorio clonado
- [ ] Backend: venv creado, dependencias instaladas
- [ ] Backend: .env configurado correctamente
- [ ] Backend: migraciones ejecutadas
- [ ] Backend: datos iniciales cargados (SMAE, equivalentes)
- [ ] Backend: servicio systemd configurado
- [ ] Frontend: dependencias instaladas
- [ ] Frontend: build de producción generado
- [ ] Nginx configurado con SSL
- [ ] Certificados SSL obtenidos (Let's Encrypt)
- [ ] Firewall configurado (UFW)
- [ ] Fail2Ban configurado
- [ ] Prometheus + Grafana desplegados
- [ ] Backups automáticos configurados
- [ ] Monitoring y alertas configurados
- [ ] Health checks funcionando
- [ ] Logs rotando correctamente
- [ ] Documentación actualizada

### 11.2 Comandos Útiles Rápidos

```bash
# Ver estado de todos los servicios
sudo systemctl status nutrition-backend postgresql redis nginx

# Logs en tiempo real
sudo journalctl -u nutrition-backend -f

# Reinicio completo
sudo systemctl restart nutrition-backend nginx

# Verificar conectividad
curl -f http://localhost:8000/health && echo "✅ OK" || echo "❌ FAIL"

# Ver conexiones activas
sudo netstat -an | grep :8000 | wc -l

# Espacio en disco
df -h | grep -E '(Filesystem|/$|/home)'

# Top procesos por CPU
ps aux --sort=-%cpu | head -10

# Top procesos por memoria
ps aux --sort=-%mem | head -10

# PostgreSQL: Número de conexiones
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname='nutrition_intelligence';"

# Redis: Info
redis-cli info | grep -E '(used_memory_human|connected_clients)'
```

### 11.3 Contactos y Escalamiento

**Nivel 1 - Soporte Técnico:**
- Email: soporte@nutrition-intelligence.com
- Slack: #soporte-tecnico
- Horario: 24/7

**Nivel 2 - Ingeniería:**
- Email: ingenieria@nutrition-intelligence.com
- Slack: #ingenieria
- Horario: Lun-Vie 9am-6pm

**Nivel 3 - DevOps/SRE:**
- Email: devops@nutrition-intelligence.com
- Slack: #devops-emergencias
- Horario: On-call 24/7

**Nivel 4 - CTO:**
- Email: cto@nutrition-intelligence.com
- Teléfono: +52 55 1234-5678
- Solo emergencias críticas

---

## 📝 Control de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | 2025-01-15 | Arquitectura | Versión inicial del manual |

---

## 📄 Referencias

- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL High Availability](https://www.postgresql.org/docs/15/high-availability.html)
- [Nginx Performance Tuning](https://www.nginx.com/blog/tuning-nginx/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [NOM-004-SSA3-2012](https://www.dof.gob.mx/nota_detalle.php?codigo=5272787&fecha=15/10/2012)

---

**Fin del Documento MD070 - Manual de Operaciones y Deployment**
