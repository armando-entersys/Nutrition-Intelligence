# Logging System - Quick Reference Card

## Backend Logging

```python
from core.logging import log_info, log_success, log_warning, log_error

# Basic
log_info("User action")
log_success("Operation completed")
log_warning("Performance degraded")
log_error("Operation failed", error=exception)

# With context
log_success(
    "Payment processed",
    user_id="12345",
    business_context={"amount": 150, "currency": "MXN"}
)
```

## Frontend Logging

```javascript
import logger from '@/utils/logger';

logger.info('Page loaded');
logger.warn('API slow', { duration: 5000 });
logger.error('Failed', error, { component: 'Dashboard' });
logger.apiError('/api/users', error);
logger.authEvent('login');
logger.pageView('Dashboard');
logger.userAction('export', { format: 'pdf' });
```

## View Logs (Docker)

```bash
# All logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log

# Errors only
docker exec -it nutrition-intelligence-backend tail -f /app/logs/error.log

# Frontend logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/frontend.log

# Pretty JSON
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log | jq '.'
```

## Manage Logs

```bash
# Check disk usage
docker exec -it nutrition-intelligence-backend du -sh /app/logs/

# Manual rotation
docker exec -it nutrition-intelligence-backend logrotate -f /etc/logrotate.d/nutrition-intelligence

# Backup logs
docker cp nutrition-intelligence-backend:/app/logs ./logs-backup

# Clean old logs (90+ days)
docker exec -it nutrition-intelligence-backend find /app/logs -name "*.gz" -mtime +90 -delete
```

## API Endpoints

```bash
# Health check
curl http://localhost:8000/api/v1/logs/health

# Send frontend log
curl -X POST http://localhost:8000/api/v1/logs/frontend \
  -H "Content-Type: application/json" \
  -d '{"logs": [{"timestamp": "2025-11-14T10:00:00Z", "level": "error", "message": "Test", "sessionId": "test"}]}'
```

## Log Analysis

```bash
# Count by level
cat app.log | jq -r '.status' | sort | uniq -c

# Top 10 slowest endpoints
cat access.log | jq -r '"\(.response_time_ms)\t\(.endpoint)"' | sort -rn | head -10

# Filter errors
cat app.log | jq 'select(.status=="Error")'

# Filter by user
cat app.log | jq 'select(.user_id=="12345")'

# Error rate per hour
cat error.log | jq -r '.timestamp[:13]' | sort | uniq -c
```

## Log Files

| File | Content | Retention |
|------|---------|-----------|
| app.log | All logs | 30 days |
| error.log | Errors only | 90 days |
| access.log | HTTP requests | 14 days |
| frontend.log | Frontend errors | 30 days |

## Troubleshooting

```bash
# Fix permissions
docker exec -it nutrition-intelligence-backend chmod 755 /app/logs

# Start cron (for logrotate)
docker exec -it nutrition-intelligence-backend service cron start

# Test logrotate
docker exec -it nutrition-intelligence-backend logrotate -d /etc/logrotate.d/nutrition-intelligence
```

## Full Documentation

- **Complete Guide:** `LOGGING_SYSTEM.md` (60+ pages)
- **Setup Guide:** `backend/LOGGING_SETUP.md`
- **Implementation Summary:** `LOGGING_IMPLEMENTATION_SUMMARY.md`
- **Test Script:** `backend/test_logging.py`

---
**Quick Access:** Keep this card handy for daily operations
