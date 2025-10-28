# 🚀 Nutrition Intelligence - Deployment Guide

## Overview

This guide covers the complete deployment and CI/CD setup for the Nutrition Intelligence platform.

## 📋 Prerequisites

### System Requirements
- Docker 20.0+
- Docker Compose 2.0+
- Git 2.30+
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Environment Setup
1. Clone the repository
2. Create environment files for each environment
3. Configure secrets and environment variables
4. Set up monitoring and logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │    │     Backend     │    │    Database     │
│   (React/Nginx) │    │   (FastAPI)     │    │  (PostgreSQL)   │
│     Port 3001   │    │   Port 8000     │    │   Port 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┐    ┌┴─────────────────┐    ┌─────────────────┐
         │     Redis       │    │      Nginx       │    │     MinIO       │
         │   (Cache)       │    │ (Load Balancer)  │    │   (Storage)     │
         │   Port 6379     │    │    Port 80/443   │    │   Port 9000     │
         └─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Environments

### Development
- **Frontend**: http://localhost:3005
- **Backend**: http://localhost:8001 (Mock)
- **Monitoring**: http://localhost:5000
- **Database**: Local development DB

### Staging
- **URL**: http://staging.nutrition-intelligence.com
- **Database**: Staging PostgreSQL
- **Monitoring**: Enhanced logging and metrics
- **Performance Testing**: Automated load tests

### Production
- **URL**: https://nutrition-intelligence.com
- **Database**: Production PostgreSQL with backups
- **Monitoring**: Full observability stack
- **High Availability**: Blue-green deployments

## 🚀 Deployment Methods

### 1. Manual Deployment

```bash
# Development
docker-compose up -d

# Staging
docker-compose -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.production.yml up -d
```

### 2. Script-based Deployment

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production

# Rollback
./scripts/deploy.sh rollback
```

### 3. CI/CD Pipeline

The GitHub Actions pipeline automatically:
- Runs tests on every push/PR
- Builds and pushes Docker images
- Deploys to staging on `develop` branch
- Deploys to production on `main` branch
- Performs security scans and performance tests

## 📊 Monitoring & Observability

### Health Monitoring
- **Health Monitor**: Background service monitoring all components
- **Dashboard**: Real-time web dashboard at port 5000
- **Metrics**: CPU, memory, disk, network, response times
- **Alerts**: Configurable thresholds with notifications

### Logging
```
logs/
├── nginx/          # Web server logs
├── backend/        # Application logs
├── postgres/       # Database logs
├── redis/          # Cache logs
├── minio/          # Storage logs
└── health_monitor.log  # Monitoring logs
```

### Metrics Collection
- **System Metrics**: CPU, memory, disk usage
- **Application Metrics**: Response times, error rates
- **Business Metrics**: API usage, user interactions
- **Performance Metrics**: Load test results

## 🔒 Security

### Container Security
- Non-root users in all containers
- Security scanning with Trivy
- Minimal base images (Alpine Linux)
- Regular security updates

### Application Security
- JWT authentication
- CORS configuration
- Input validation
- SQL injection protection
- XSS protection headers

### Infrastructure Security
- SSL/TLS encryption
- Database encryption at rest
- Secrets management
- Network isolation

## 🧪 Testing Strategy

### Unit Tests
- **Backend**: pytest with coverage
- **Frontend**: Jest with React Testing Library
- **Coverage**: >80% target

### Integration Tests
- API endpoint testing
- Database integration tests
- Authentication flow tests

### Performance Tests
- Load testing with k6
- Response time benchmarks
- Stress testing scenarios

### Security Tests
- Vulnerability scanning
- Penetration testing
- Dependency security checks

## 🔄 CI/CD Pipeline

### Pipeline Stages

1. **Code Quality**
   - Linting (ESLint, Ruff)
   - Type checking (TypeScript, mypy)
   - Code formatting (Prettier, Black)

2. **Testing**
   - Unit tests with coverage
   - Integration tests
   - Security scans

3. **Build**
   - Docker image builds
   - Multi-stage optimized builds
   - Image scanning

4. **Deploy**
   - Staging deployment (develop branch)
   - Production deployment (main branch)
   - Blue-green deployments for zero-downtime

5. **Verify**
   - Health checks
   - Smoke tests
   - Performance validation

### GitHub Actions Configuration

Required secrets:
```
DOCKER_USERNAME
DOCKER_PASSWORD
STAGING_HOST
STAGING_USER
STAGING_SSH_KEY
PRODUCTION_HOST
PRODUCTION_USER
PRODUCTION_SSH_KEY
SLACK_WEBHOOK
```

## 🗄️ Database Management

### Migrations
```bash
# Run migrations
docker exec nutrition-backend alembic upgrade head

# Create new migration
docker exec nutrition-backend alembic revision --autogenerate -m "description"
```

### Backups
```bash
# Manual backup
docker exec nutrition-postgres pg_dump -U nutrition_user nutrition_db > backup.sql

# Automated backups (configured in production)
# Daily backups with 30-day retention
```

### Restore
```bash
# Restore from backup
cat backup.sql | docker exec -i nutrition-postgres psql -U nutrition_user -d nutrition_db
```

## 📱 Current Service Status

### Running Services
- ✅ **Frontend**: http://localhost:3005
- ✅ **Mock Backend**: http://localhost:8001
- ✅ **Health Monitor**: Background process
- ✅ **Monitoring Dashboard**: http://localhost:5000

### Service Ports
```
3005  - Frontend (React)
8001  - Mock Backend (Python)
5000  - Monitoring Dashboard
8000  - Real Backend (when running)
5432  - PostgreSQL
6379  - Redis
9000  - MinIO API
9001  - MinIO Console
```

## 🚨 Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Check if mock backend is running on port 8001
   - Verify CORS configuration
   - Check network connectivity

2. **Database Connection Issues**
   - Verify PostgreSQL container is running
   - Check database credentials
   - Ensure proper network configuration

3. **Frontend Build Failures**
   - Check Node.js version compatibility
   - Clear npm cache: `npm cache clean --force`
   - Verify environment variables

4. **Docker Issues**
   - Free up disk space
   - Restart Docker daemon
   - Check container logs: `docker logs <container-name>`

### Health Checks

```bash
# Check all services
./scripts/deploy.sh health

# Individual service checks
curl http://localhost:8001/health        # Backend
curl http://localhost:3005/              # Frontend
curl http://localhost:5000/api/health    # Monitoring
```

## 📈 Performance Optimization

### Backend Optimization
- Connection pooling
- Query optimization
- Caching strategies
- Async processing

### Frontend Optimization
- Code splitting
- Lazy loading
- Asset optimization
- CDN integration

### Database Optimization
- Index optimization
- Query analysis
- Connection pooling
- Read replicas

## 🔮 Future Enhancements

### Planned Features
- [ ] Kubernetes deployment
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] AI-powered recommendations
- [ ] Multi-tenant architecture

### Infrastructure Improvements
- [ ] Auto-scaling
- [ ] Multi-region deployment
- [ ] Advanced monitoring (Prometheus/Grafana)
- [ ] Log aggregation (ELK stack)
- [ ] Service mesh (Istio)

## 📞 Support

### Documentation
- API Documentation: http://localhost:8001/docs
- Frontend Documentation: `/frontend/README.md`
- Backend Documentation: `/backend/README.md`

### Monitoring
- System Dashboard: http://localhost:5000
- Health Status: http://localhost:8001/health
- Performance Metrics: Available in dashboard

### Logs
- Application logs: `./logs/`
- Container logs: `docker logs <container-name>`
- System logs: Available in monitoring dashboard

---

**Last Updated**: 2025-09-28
**Version**: 1.0.0
**Platform**: Nutrition Intelligence