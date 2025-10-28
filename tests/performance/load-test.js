import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 20 }, // Ramp up to 20 users
    { duration: '5m', target: 20 }, // Stay at 20 users
    { duration: '2m', target: 50 }, // Ramp up to 50 users
    { duration: '5m', target: 50 }, // Stay at 50 users
    { duration: '2m', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],    // Error rate should be below 10%
    errors: ['rate<0.1'],             // Custom error rate should be below 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

export default function () {
  // Test health endpoint
  let healthResponse = http.get(`${BASE_URL}/health`);
  let healthCheck = check(healthResponse, {
    'health endpoint status is 200': (r) => r.status === 200,
    'health endpoint response time < 200ms': (r) => r.timings.duration < 200,
  });
  errorRate.add(!healthCheck);

  sleep(1);

  // Test foods API endpoint
  let foodsResponse = http.get(`${BASE_URL}/api/v1/foods`);
  let foodsCheck = check(foodsResponse, {
    'foods endpoint status is 200': (r) => r.status === 200,
    'foods endpoint response time < 500ms': (r) => r.timings.duration < 500,
    'foods endpoint returns array': (r) => {
      try {
        const data = JSON.parse(r.body);
        return Array.isArray(data);
      } catch (e) {
        return false;
      }
    },
  });
  errorRate.add(!foodsCheck);

  sleep(1);

  // Test frontend
  let frontendResponse = http.get(`${BASE_URL}/`);
  let frontendCheck = check(frontendResponse, {
    'frontend status is 200': (r) => r.status === 200,
    'frontend response time < 1000ms': (r) => r.timings.duration < 1000,
  });
  errorRate.add(!frontendCheck);

  sleep(2);
}