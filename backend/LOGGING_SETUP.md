# Logging System Setup Guide

Quick setup guide for the Nutrition Intelligence logging system.

## Prerequisites

- Docker and Docker Compose installed
- Backend already configured

## Setup Steps

### 1. Development Environment

The logging system is already configured. Just verify it works:

```bash
# Navigate to backend
cd backend

# Run test script
python test_logging.py

# Check logs were created
ls -lh logs/

# View logs
tail -f logs/app.log
```

### 2. Production Environment (Docker)

The logging system is automatically set up when you build the Docker container:

```bash
# Build and start containers
docker-compose up -d --build

# Verify logs directory exists
docker exec -it nutrition-intelligence-backend ls -lh /app/logs/

# View logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log

# Check logrotate configuration
docker exec -it nutrition-intelligence-backend cat /etc/logrotate.d/nutrition-intelligence
```

### 3. Enable Cron for Log Rotation

If logrotate isn't running automatically, enable cron:

```bash
# Enter container
docker exec -it nutrition-intelligence-backend bash

# Start cron service
service cron start

# Enable cron on container startup (add to entrypoint)
# Or modify CMD in Dockerfile:
# CMD ["sh", "-c", "service cron start && uvicorn main:app --host 0.0.0.0 --port 8000"]
```

### 4. Frontend Logger Setup

The frontend logger is already configured. Just import and use:

```javascript
// In your React components
import logger from '@/utils/logger';

// Use anywhere in your code
logger.info('Component mounted');
logger.error('Failed to load data', error);
```

### 5. Test Frontend Logging

```javascript
// Add to your App.js or main component
import { useEffect } from 'react';
import logger from './utils/logger';

function App() {
  useEffect(() => {
    logger.info('Application started');

    // Test error logging
    setTimeout(() => {
      logger.error('Test error', new Error('This is a test'), {
        component: 'App',
        test: true
      });
    }, 5000);
  }, []);

  // ... rest of your app
}
```

### 6. Verify Frontend Logs Endpoint

```bash
# Check endpoint health
curl http://localhost:8000/api/v1/logs/health

# Send test log
curl -X POST http://localhost:8000/api/v1/logs/frontend \
  -H "Content-Type: application/json" \
  -d '{
    "logs": [{
      "timestamp": "2025-11-14T10:00:00Z",
      "level": "error",
      "message": "Test error from curl",
      "user": {
        "userId": "test-123"
      },
      "browser": {
        "userAgent": "curl/7.0"
      },
      "sessionId": "test-session"
    }]
  }'

# Check frontend log file
docker exec -it nutrition-intelligence-backend cat /app/logs/frontend.log
```

## Verification Checklist

- [ ] Backend logs directory created (`/app/logs` or `logs/`)
- [ ] Log files created (app.log, error.log, access.log)
- [ ] Logs contain JSON-formatted entries
- [ ] LoggingMiddleware capturing HTTP requests
- [ ] Logrotate configuration installed
- [ ] Frontend logger imported and working
- [ ] Frontend logs endpoint responding (200 OK)
- [ ] Frontend errors appearing in frontend.log
- [ ] Docker volume persisting logs

## Common Issues

### Issue: Logs directory doesn't exist

```bash
# Create manually
docker exec -it nutrition-intelligence-backend mkdir -p /app/logs
docker exec -it nutrition-intelligence-backend chmod 755 /app/logs
```

### Issue: Permission denied writing logs

```bash
# Fix permissions
docker exec -it nutrition-intelligence-backend chmod 755 /app/logs
docker exec -it nutrition-intelligence-backend chown -R root:root /app/logs
```

### Issue: Frontend logs not reaching backend

1. Check REACT_APP_API_URL environment variable
2. Verify backend is running
3. Check CORS configuration
4. Check rate limiting (wait 1 minute)

### Issue: Logrotate not working

```bash
# Test configuration
docker exec -it nutrition-intelligence-backend logrotate -d /etc/logrotate.d/nutrition-intelligence

# Check cron
docker exec -it nutrition-intelligence-backend service cron status

# Start cron
docker exec -it nutrition-intelligence-backend service cron start
```

## Next Steps

1. Monitor logs for a few days
2. Adjust retention policies if needed
3. Set up log monitoring/alerting (optional)
4. Configure log aggregation (ELK, Loki, etc.) for production

## Quick Reference

### View Logs

```bash
# All logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log

# Errors only
docker exec -it nutrition-intelligence-backend tail -f /app/logs/error.log

# Frontend logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/frontend.log

# Pretty print JSON
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log | jq '.'
```

### Manage Logs

```bash
# Check disk usage
docker exec -it nutrition-intelligence-backend du -sh /app/logs/

# Manual rotation
docker exec -it nutrition-intelligence-backend logrotate -f /etc/logrotate.d/nutrition-intelligence

# Clean old logs
docker exec -it nutrition-intelligence-backend find /app/logs -name "*.gz" -mtime +90 -delete

# Backup logs
docker cp nutrition-intelligence-backend:/app/logs ./backup-logs-$(date +%Y%m%d)
```

## Support

For detailed documentation, see [LOGGING_SYSTEM.md](../LOGGING_SYSTEM.md)
