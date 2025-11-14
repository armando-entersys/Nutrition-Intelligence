# Logging System Documentation
## Nutrition Intelligence Platform

This document describes the comprehensive logging system implemented for the Nutrition Intelligence platform, including backend structured logging, log rotation, and frontend error reporting.

## Overview

The logging system provides:
- **Structured JSON logging** for easy parsing and analysis
- **Automatic log rotation** to prevent disk space issues
- **Separate log files** for different log types (app, error, access, frontend)
- **FastAPI middleware** for automatic request/response logging
- **Frontend error reporting** to backend
- **Rate limiting** to prevent log flooding
- **Production-ready** with Docker volume persistence

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Application                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  logger.js - Frontend Logging Service            │  │
│  │  • Console logs (development)                     │  │
│  │  • Backend reporting (production)                 │  │
│  │  • Automatic error capture                        │  │
│  └───────────────┬─────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────┘
                     │ HTTP POST
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend API                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  /api/v1/logs/frontend - Log Receiver Endpoint   │  │
│  │  • Rate limited (20 req/min)                      │  │
│  │  • Validates & stores logs                        │  │
│  └───────────────┬─────────────────────────────────┘  │
│                  │                                       │
│  ┌───────────────▼─────────────────────────────────┐  │
│  │  core/logging.py - Logging System               │  │
│  │  • RotatingFileHandler (10MB, 5 backups)        │  │
│  │  • JSON structured logging                       │  │
│  │  • LoggingMiddleware for requests                │  │
│  └───────────────┬─────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 Log Files (/app/logs/)                  │
│  • app.log       - General application logs             │
│  • error.log     - Error-level logs only                │
│  • access.log    - HTTP request/response logs           │
│  • frontend.log  - Frontend error reports               │
│                                                          │
│  Rotation: logrotate daily (30 days retention)          │
└─────────────────────────────────────────────────────────┘
```

## Backend Logging System

### File: `backend/core/logging.py`

The core logging module provides structured logging with rotation and middleware.

#### Features

1. **Rotating File Handlers**
   - Max file size: 10MB
   - Backup count: 5 files
   - Automatic rotation when size exceeded

2. **Multiple Log Files**
   - `app.log` - All INFO+ logs
   - `error.log` - ERROR+ logs only
   - `access.log` - HTTP access logs

3. **JSON Structured Logging**
   ```json
   {
     "timestamp": "2025-11-14T10:30:45.123Z",
     "level": "INFO",
     "logger": "nutrition_intelligence",
     "message": "User login successful",
     "module": "auth",
     "function": "login",
     "line": 42,
     "request_id": "uuid-here",
     "user_id": "12345",
     "business_context": {
       "action": "user_login",
       "success": true
     }
   }
   ```

#### Usage

```python
from core.logging import log_info, log_success, log_warning, log_error

# Simple logging
log_info("Processing request")

# With context
log_success(
    "User registered successfully",
    user_id="12345",
    business_context={"action": "registration", "role": "patient"}
)

# Error logging
try:
    risky_operation()
except Exception as e:
    log_error(
        "Failed to process operation",
        error=e,
        user_id="12345",
        business_context={"operation": "data_sync"}
    )

# Warning logging
log_warning(
    "Rate limit approaching",
    user_id="12345",
    business_context={"remaining_requests": 5}
)
```

### LoggingMiddleware

Automatically logs all HTTP requests and responses.

```python
from core.logging import LoggingMiddleware

app.add_middleware(LoggingMiddleware)
```

Captures:
- HTTP method and endpoint
- Status code
- Response time (ms)
- Client IP and User-Agent
- User ID (if authenticated)
- Request ID for tracing

## Frontend Logging System

### File: `frontend/src/utils/logger.js`

Client-side logging service with backend error reporting.

#### Features

1. **Environment-Aware**
   - Development: Console logging only
   - Production: Backend error reporting

2. **Rate Limited**
   - Max 50 logs in queue
   - Flush every 5 seconds
   - Immediate flush for errors

3. **Automatic Error Capture**
   - Global error handler
   - Unhandled promise rejections
   - User context included

#### Usage

```javascript
import logger from '@/utils/logger';

// Info logging (console only in dev)
logger.info('User viewed dashboard');

// Warning (sent to backend in prod)
logger.warn('API response slow', { duration: 5000 });

// Error logging (always sent to backend)
logger.error('Failed to load data', error, { endpoint: '/api/data' });

// Specialized loggers
logger.apiError('/api/users', error, { userId: '123' });
logger.authEvent('login', { method: 'email' });
logger.pageView('Dashboard');
logger.userAction('export_report', { format: 'pdf' });
logger.performance('data_load', 1250);
```

#### Automatic Features

```javascript
// Global error handler - automatically logs uncaught errors
window.addEventListener('error', (event) => {
  // Automatically captured and logged
});

// Unhandled promise rejections - automatically logged
window.addEventListener('unhandledrejection', (event) => {
  // Automatically captured and logged
});

// Session tracking
// Automatically generates sessionId on first load
```

## Frontend Log Endpoint

### File: `backend/api/routers/logs.py`

Receives and stores frontend logs.

#### Endpoint

```
POST /api/v1/logs/frontend
```

**Rate Limit:** 20 requests per minute

**Request Body:**
```json
{
  "logs": [
    {
      "timestamp": "2025-11-14T10:30:45.123Z",
      "level": "error",
      "message": "Failed to fetch user data",
      "user": {
        "userId": "12345",
        "email": "user@example.com",
        "role": "patient"
      },
      "browser": {
        "userAgent": "Mozilla/5.0...",
        "language": "es-MX",
        "platform": "Win32",
        "screenResolution": "1920x1080",
        "viewport": "1200x800",
        "url": "https://app.example.com/dashboard",
        "referrer": "https://app.example.com/login"
      },
      "context": {
        "endpoint": "/api/v1/users/me",
        "error": {
          "name": "NetworkError",
          "message": "Failed to fetch",
          "stack": "..."
        }
      },
      "sessionId": "session_1234567890_abc123"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Received 1 logs",
  "logs_received": 1,
  "errors": null
}
```

#### Health Check

```
GET /api/v1/logs/health
```

Returns logging system status:
```json
{
  "status": "healthy",
  "frontend_log_file": "/app/logs/frontend.log",
  "log_file_exists": true,
  "log_dir_writable": true,
  "max_log_size_mb": 10,
  "backup_count": 5
}
```

## Log Rotation Configuration

### File: `backend/logrotate.conf`

Logrotate configuration for automatic log management.

#### Configuration Details

| Log File | Rotation | Retention | Max Size | Compression |
|----------|----------|-----------|----------|-------------|
| app.log | Daily | 30 days | - | Yes (gzip) |
| error.log | Daily | 90 days | - | Yes (gzip) |
| access.log | Daily | 14 days | 50MB | Yes (gzip) |
| frontend.log | Daily | 30 days | 100MB | Yes (gzip) |

#### Features

- **Daily rotation** - Logs rotated every day
- **Compression** - Old logs compressed with gzip
- **Delayed compression** - Previous day's log not compressed (for easy access)
- **Date extension** - Rotated files named with date (e.g., `app.log-20251114.gz`)
- **Graceful reload** - Sends SIGHUP to processes after rotation

#### Manual Rotation

```bash
# Test logrotate configuration
logrotate -d /etc/logrotate.d/nutrition-intelligence

# Force rotation
logrotate -f /etc/logrotate.d/nutrition-intelligence

# Run rotation (normally done by cron)
logrotate /etc/logrotate.d/nutrition-intelligence
```

## Docker Configuration

### Dockerfile Updates

```dockerfile
# Install logrotate and cron
RUN apt-get update && apt-get install -y \
    logrotate \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && \
    chmod 755 /app/logs

# Copy logrotate configuration
COPY logrotate.conf /etc/logrotate.d/nutrition-intelligence
RUN chmod 644 /etc/logrotate.d/nutrition-intelligence
```

### Docker Compose Volume

```yaml
services:
  backend:
    volumes:
      - ./backend:/app
      - backend_data:/app/data
      - backend_logs:/app/logs  # Persistent logs volume

volumes:
  backend_logs:
    name: nutrition_intelligence_backend_logs
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect logs volume
docker volume inspect nutrition_intelligence_backend_logs

# Access logs from host
docker exec -it nutrition-intelligence-backend ls -lh /app/logs/

# View logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log

# Copy logs to host
docker cp nutrition-intelligence-backend:/app/logs ./local-logs

# Backup logs volume
docker run --rm -v nutrition_intelligence_backend_logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/logs-backup-$(date +%Y%m%d).tar.gz /data

# Clean up old logs (if needed)
docker exec -it nutrition-intelligence-backend find /app/logs -name "*.gz" -mtime +90 -delete
```

## Log Monitoring

### View Logs in Real-Time

```bash
# Backend app logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log

# Error logs only
docker exec -it nutrition-intelligence-backend tail -f /app/logs/error.log

# Access logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/access.log

# Frontend error logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/frontend.log

# All logs combined
docker exec -it nutrition-intelligence-backend tail -f /app/logs/*.log
```

### Parse JSON Logs

```bash
# Pretty print JSON logs
docker exec -it nutrition-intelligence-backend tail -f /app/logs/app.log | jq '.'

# Filter by level
docker exec -it nutrition-intelligence-backend cat /app/logs/app.log | jq 'select(.level=="ERROR")'

# Filter by user
docker exec -it nutrition-intelligence-backend cat /app/logs/app.log | jq 'select(.user_id=="12345")'

# Filter by time range
docker exec -it nutrition-intelligence-backend cat /app/logs/app.log | jq 'select(.timestamp >= "2025-11-14T00:00:00")'

# Count errors by type
docker exec -it nutrition-intelligence-backend cat /app/logs/error.log | jq -r '.exception.type' | sort | uniq -c
```

### Log Analysis

```bash
# Count log entries by level
cat app.log | jq -r '.level' | sort | uniq -c

# Top 10 slowest endpoints
cat access.log | jq -r '"\(.duration_ms)\t\(.endpoint)"' | sort -rn | head -10

# Error rate per hour
cat error.log | jq -r '.timestamp[:13]' | sort | uniq -c

# Most common error messages
cat error.log | jq -r '.message' | sort | uniq -c | sort -rn | head -20

# Frontend errors by browser
cat frontend.log | jq -r '.browser.userAgent' | sort | uniq -c
```

## Integration with Monitoring Tools

### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# docker-compose.elk.yml
services:
  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    volumes:
      - backend_logs:/app/logs:ro
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
    depends_on:
      - elasticsearch

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
```

### Grafana Loki

```yaml
services:
  promtail:
    image: grafana/promtail:latest
    volumes:
      - backend_logs:/app/logs:ro
      - ./promtail-config.yml:/etc/promtail/config.yml:ro

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

## Troubleshooting

### Issue: Logs not rotating

**Solution:**
```bash
# Check logrotate configuration
logrotate -d /etc/logrotate.d/nutrition-intelligence

# Check cron service
docker exec -it nutrition-intelligence-backend service cron status

# Manually trigger rotation
docker exec -it nutrition-intelligence-backend logrotate -f /etc/logrotate.d/nutrition-intelligence
```

### Issue: Log directory permissions

**Solution:**
```bash
# Fix permissions
docker exec -it nutrition-intelligence-backend chmod 755 /app/logs
docker exec -it nutrition-intelligence-backend chown -R root:root /app/logs
```

### Issue: Disk space full

**Solution:**
```bash
# Check disk usage
docker exec -it nutrition-intelligence-backend du -sh /app/logs/*

# Manually clean old logs
docker exec -it nutrition-intelligence-backend find /app/logs -name "*.gz" -mtime +30 -delete

# Compress current logs
docker exec -it nutrition-intelligence-backend gzip /app/logs/*.log-*
```

### Issue: Frontend logs not received

**Solution:**
```bash
# Check endpoint health
curl http://localhost:8000/api/v1/logs/health

# Check rate limiting
# Wait 1 minute and retry

# Verify frontend configuration
# Check REACT_APP_API_URL environment variable
```

## Best Practices

### Backend Logging

1. **Use structured logging** with business context
   ```python
   log_success(
       "Payment processed",
       user_id=user.id,
       business_context={
           "amount": payment.amount,
           "currency": payment.currency,
           "transaction_id": payment.id
       }
   )
   ```

2. **Include request_id** for request tracing
   ```python
   request_id = request.state.request_id
   log_error("Database error", error=e, request_id=request_id)
   ```

3. **Log business events**, not just technical events
   ```python
   log_success("Meal plan created", business_context={
       "patient_id": patient.id,
       "nutritionist_id": nutritionist.id,
       "plan_type": "weight_loss"
   })
   ```

4. **Don't log sensitive data** (passwords, tokens, PII)
   ```python
   # Bad
   log_info(f"User logged in: {user.email}, password: {password}")

   # Good
   log_info("User logged in", user_id=user.id)
   ```

### Frontend Logging

1. **Use appropriate log levels**
   ```javascript
   logger.info('Page loaded');  // Informational
   logger.warn('API slow', { duration });  // Warning
   logger.error('Failed to load', error);  // Error
   ```

2. **Include context for debugging**
   ```javascript
   logger.error('API error', error, {
       endpoint: '/api/users',
       method: 'POST',
       status: response.status,
       data: sanitizedData  // Remove sensitive fields
   });
   ```

3. **Log user actions** for analytics
   ```javascript
   logger.userAction('export_report', {
       format: 'pdf',
       dateRange: '30days'
   });
   ```

4. **Avoid logging in loops**
   ```javascript
   // Bad
   data.forEach(item => logger.info('Processing', item));

   // Good
   logger.info('Processing batch', { count: data.length });
   ```

## Security Considerations

1. **Rate Limiting** - Frontend log endpoint is rate limited (20 req/min)
2. **Input Validation** - All log entries validated before storage
3. **Size Limits** - Max 50 logs per request, 1000 chars per message
4. **Sanitization** - Sensitive data should be removed before logging
5. **Access Control** - Log files only accessible to authorized personnel
6. **Encryption** - Logs stored in encrypted volumes in production

## Performance Impact

- **Backend Logging:** Minimal (~1-2ms per log entry)
- **LoggingMiddleware:** ~0.5ms per request
- **Frontend Logging:** Async, no blocking (queued and batched)
- **Log Rotation:** Runs daily during low-traffic hours
- **Disk Usage:** ~100-500MB/day for typical workload

## Maintenance Schedule

- **Daily:** Automatic log rotation via cron
- **Weekly:** Review error logs for patterns
- **Monthly:** Archive old compressed logs to cold storage
- **Quarterly:** Review and optimize log retention policies

## Support

For issues or questions about the logging system:
1. Check this documentation
2. Review logs: `docker logs nutrition-intelligence-backend`
3. Check log health: `GET /api/v1/logs/health`
4. Contact DevOps team

---

**Last Updated:** November 14, 2025
**Version:** 1.0.0
**Maintainer:** DevOps Team
