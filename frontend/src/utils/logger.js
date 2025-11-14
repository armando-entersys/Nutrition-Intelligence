/**
 * Frontend Logging Service for Nutrition Intelligence Platform
 * Provides structured logging with console output in development
 * and backend error reporting in production
 */

const LOG_LEVELS = {
  INFO: 'info',
  WARN: 'warn',
  ERROR: 'error',
  DEBUG: 'debug'
};

// Check if we're in production
const isProduction = process.env.NODE_ENV === 'production';
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const FRONTEND_LOG_ENDPOINT = `${API_BASE_URL}/api/v1/logs/frontend`;

// Rate limiting for backend logging (prevent spam)
const LOG_QUEUE = [];
const MAX_QUEUE_SIZE = 50;
const FLUSH_INTERVAL = 5000; // 5 seconds
let lastFlushTime = Date.now();

/**
 * Get user context from session/local storage
 * @returns {Object} User context object
 */
const getUserContext = () => {
  try {
    const userStr = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      return {
        userId: user.id,
        email: user.email,
        role: user.role
      };
    }
  } catch (error) {
    // Silently fail if user context is not available
  }
  return {
    userId: null,
    email: null,
    role: null
  };
};

/**
 * Get browser and system information
 * @returns {Object} Browser context object
 */
const getBrowserContext = () => {
  return {
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenResolution: `${window.screen.width}x${window.screen.height}`,
    viewport: `${window.innerWidth}x${window.innerHeight}`,
    url: window.location.href,
    referrer: document.referrer
  };
};

/**
 * Format log entry with structured data
 * @param {string} level - Log level
 * @param {string} message - Log message
 * @param {Object} context - Additional context
 * @returns {Object} Formatted log entry
 */
const formatLogEntry = (level, message, context = {}) => {
  return {
    timestamp: new Date().toISOString(),
    level,
    message,
    user: getUserContext(),
    browser: getBrowserContext(),
    context,
    sessionId: sessionStorage.getItem('sessionId') || 'unknown'
  };
};

/**
 * Send logs to backend
 * @param {Array} logs - Array of log entries
 */
const sendLogsToBackend = async (logs) => {
  if (!isProduction || logs.length === 0) {
    return;
  }

  try {
    const response = await fetch(FRONTEND_LOG_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Include auth token if available
        ...(localStorage.getItem('token') && {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        })
      },
      body: JSON.stringify({ logs })
    });

    if (!response.ok) {
      console.error('Failed to send logs to backend:', response.statusText);
    }
  } catch (error) {
    // Silently fail - don't want logging errors to break the app
    console.error('Error sending logs to backend:', error);
  }
};

/**
 * Flush log queue to backend
 */
const flushLogQueue = () => {
  if (LOG_QUEUE.length === 0) {
    return;
  }

  const logsToSend = [...LOG_QUEUE];
  LOG_QUEUE.length = 0;
  lastFlushTime = Date.now();

  sendLogsToBackend(logsToSend);
};

/**
 * Add log to queue and flush if needed
 * @param {Object} logEntry - Log entry to queue
 */
const queueLog = (logEntry) => {
  // Only queue errors and warnings in production
  if (isProduction && (logEntry.level === LOG_LEVELS.ERROR || logEntry.level === LOG_LEVELS.WARN)) {
    LOG_QUEUE.push(logEntry);

    // Flush if queue is full or interval elapsed
    if (LOG_QUEUE.length >= MAX_QUEUE_SIZE || Date.now() - lastFlushTime >= FLUSH_INTERVAL) {
      flushLogQueue();
    }
  }
};

/**
 * Log info message
 * @param {string} message - Log message
 * @param {Object} context - Additional context
 */
export const logInfo = (message, context = {}) => {
  const logEntry = formatLogEntry(LOG_LEVELS.INFO, message, context);

  if (!isProduction) {
    console.log(`[INFO] ${message}`, context);
  }

  // Info logs are not sent to backend by default (too verbose)
  // Can be enabled by uncommenting: queueLog(logEntry);
};

/**
 * Log warning message
 * @param {string} message - Log message
 * @param {Object} context - Additional context
 */
export const logWarn = (message, context = {}) => {
  const logEntry = formatLogEntry(LOG_LEVELS.WARN, message, context);

  console.warn(`[WARN] ${message}`, context);
  queueLog(logEntry);
};

/**
 * Log error message
 * @param {string} message - Log message
 * @param {Error|Object} error - Error object or additional context
 * @param {Object} context - Additional context
 */
export const logError = (message, error = null, context = {}) => {
  const errorContext = {
    ...context,
    error: error ? {
      name: error.name,
      message: error.message,
      stack: error.stack,
      ...error
    } : null
  };

  const logEntry = formatLogEntry(LOG_LEVELS.ERROR, message, errorContext);

  console.error(`[ERROR] ${message}`, error, context);
  queueLog(logEntry);

  // For errors, flush immediately in production
  if (isProduction) {
    flushLogQueue();
  }
};

/**
 * Log debug message (only in development)
 * @param {string} message - Log message
 * @param {Object} context - Additional context
 */
export const logDebug = (message, context = {}) => {
  if (!isProduction) {
    const logEntry = formatLogEntry(LOG_LEVELS.DEBUG, message, context);
    console.debug(`[DEBUG] ${message}`, context);
  }
};

/**
 * Log API error
 * @param {string} endpoint - API endpoint
 * @param {Error} error - Error object
 * @param {Object} requestData - Request data
 */
export const logApiError = (endpoint, error, requestData = {}) => {
  logError(
    `API Error: ${endpoint}`,
    error,
    {
      endpoint,
      requestData,
      apiError: true
    }
  );
};

/**
 * Log authentication event
 * @param {string} event - Auth event type (login, logout, etc.)
 * @param {Object} context - Additional context
 */
export const logAuthEvent = (event, context = {}) => {
  logInfo(
    `Auth Event: ${event}`,
    {
      event,
      authEvent: true,
      ...context
    }
  );
};

/**
 * Log page view
 * @param {string} pageName - Page name or route
 * @param {Object} context - Additional context
 */
export const logPageView = (pageName, context = {}) => {
  logInfo(
    `Page View: ${pageName}`,
    {
      pageName,
      pageView: true,
      ...context
    }
  );
};

/**
 * Log user action
 * @param {string} action - Action name
 * @param {Object} context - Additional context
 */
export const logUserAction = (action, context = {}) => {
  logInfo(
    `User Action: ${action}`,
    {
      action,
      userAction: true,
      ...context
    }
  );
};

/**
 * Log performance metric
 * @param {string} metric - Metric name
 * @param {number} value - Metric value
 * @param {Object} context - Additional context
 */
export const logPerformance = (metric, value, context = {}) => {
  logInfo(
    `Performance: ${metric} = ${value}ms`,
    {
      metric,
      value,
      performance: true,
      ...context
    }
  );
};

// Set up periodic flush
if (isProduction) {
  setInterval(flushLogQueue, FLUSH_INTERVAL);
}

// Flush logs before page unload
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    flushLogQueue();
  });

  // Generate session ID if not exists
  if (!sessionStorage.getItem('sessionId')) {
    sessionStorage.setItem('sessionId', `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  }
}

// Global error handler
if (typeof window !== 'undefined') {
  window.addEventListener('error', (event) => {
    logError(
      'Uncaught Error',
      event.error,
      {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        globalError: true
      }
    );
  });

  // Unhandled promise rejection handler
  window.addEventListener('unhandledrejection', (event) => {
    logError(
      'Unhandled Promise Rejection',
      event.reason,
      {
        promise: true,
        globalError: true
      }
    );
  });
}

// Export logger object
const logger = {
  info: logInfo,
  warn: logWarn,
  error: logError,
  debug: logDebug,
  apiError: logApiError,
  authEvent: logAuthEvent,
  pageView: logPageView,
  userAction: logUserAction,
  performance: logPerformance,
  flush: flushLogQueue
};

export default logger;
