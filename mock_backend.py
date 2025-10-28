#!/usr/bin/env python3
"""
Mock backend server for testing frontend connectivity
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "nutrition-intelligence-api",
                "version": "1.0.0",
                "timestamp": "2025-09-28T20:00:00Z"
            }
            self.wfile.write(json.dumps(response).encode())

        elif self.path.startswith('/api/v1/foods'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Mock foods data
            foods = [
                {
                    "id": 1,
                    "name": "Manzana",
                    "category": "FRUITS",
                    "status": "APPROVED",
                    "calories_per_100g": 52,
                    "protein_per_100g": 0.3,
                    "carbs_per_100g": 14.0,
                    "fat_per_100g": 0.2
                },
                {
                    "id": 2,
                    "name": "Platano",
                    "category": "FRUITS",
                    "status": "APPROVED",
                    "calories_per_100g": 89,
                    "protein_per_100g": 1.1,
                    "carbs_per_100g": 23.0,
                    "fat_per_100g": 0.3
                }
            ]
            self.wfile.write(json.dumps(foods).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[MOCK BACKEND] {self.client_address[0]} - {format % args}")

def run_server():
    server = HTTPServer(('0.0.0.0', 8001), MockHandler)
    print("Mock Backend running on http://localhost:8001")
    print("Health check: http://localhost:8001/health")
    print("Foods API: http://localhost:8001/api/v1/foods")
    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMock Backend stopped")
        server.shutdown()

if __name__ == "__main__":
    run_server()