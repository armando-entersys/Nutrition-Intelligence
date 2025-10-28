#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for Nutrition Intelligence
Web-based dashboard for monitoring system health and performance
"""
from flask import Flask, render_template, jsonify
import json
import os
import glob
from datetime import datetime, timedelta
import psutil

app = Flask(__name__)

def get_latest_report():
    """Get the most recent health report"""
    try:
        report_files = glob.glob("logs/health_report_*.json")
        if not report_files:
            return None

        latest_file = max(report_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading health report: {e}")
        return None

def get_system_status():
    """Get current system status"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting system status: {e}")
        return None

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/health')
def api_health():
    """API endpoint for health data"""
    report = get_latest_report()
    if report:
        return jsonify(report)
    else:
        return jsonify({"error": "No health data available"}), 503

@app.route('/api/system')
def api_system():
    """API endpoint for real-time system data"""
    status = get_system_status()
    if status:
        return jsonify(status)
    else:
        return jsonify({"error": "Unable to get system status"}), 503

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for current alerts"""
    report = get_latest_report()
    if report and 'alerts' in report:
        return jsonify({"alerts": report['alerts']})
    else:
        return jsonify({"alerts": []})

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)

    # Create dashboard template
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nutrition Intelligence - Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .status-indicator {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        }

        .status-healthy {
            background: #27ae60;
            color: white;
        }

        .status-degraded {
            background: #f39c12;
            color: white;
        }

        .status-error {
            background: #e74c3c;
            color: white;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 5px;
        }

        .metric-label {
            font-weight: 500;
        }

        .metric-value {
            font-weight: bold;
            color: #2c3e50;
        }

        .service-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }

        .service-healthy {
            border-left-color: #27ae60;
        }

        .service-unhealthy {
            border-left-color: #e74c3c;
        }

        .alerts {
            background: rgba(231, 76, 60, 0.1);
            border: 1px solid #e74c3c;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }

        .alert-item {
            padding: 8px;
            margin-bottom: 5px;
            background: rgba(231, 76, 60, 0.1);
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background: #ecf0f1;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }

        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }

        .progress-normal {
            background: #27ae60;
        }

        .progress-warning {
            background: #f39c12;
        }

        .progress-critical {
            background: #e74c3c;
        }

        .last-updated {
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 20px;
        }

        .loading {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Nutrition Intelligence - System Monitor</h1>
            <div>
                <span>Overall Status: </span>
                <span id="overall-status" class="status-indicator">Loading...</span>
            </div>
        </div>

        <div class="dashboard-grid">
            <div class="card">
                <h3>System Resources</h3>
                <div id="system-metrics" class="loading">Loading system metrics...</div>
            </div>

            <div class="card">
                <h3>Services Status</h3>
                <div id="services-status" class="loading">Loading services...</div>
            </div>

            <div class="card">
                <h3>Performance</h3>
                <div id="performance-metrics" class="loading">Loading performance data...</div>
            </div>
        </div>

        <div id="alerts-section" style="display: none;">
            <div class="alerts">
                <h3>Active Alerts</h3>
                <div id="alerts-list"></div>
            </div>
        </div>

        <div class="last-updated" id="last-updated">
            Loading...
        </div>
    </div>

    <script>
        let lastUpdate = null;

        function updateStatus() {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('overall-status').textContent = 'Error';
                        document.getElementById('overall-status').className = 'status-indicator status-error';
                        return;
                    }

                    // Update overall status
                    const statusElement = document.getElementById('overall-status');
                    statusElement.textContent = data.overall_status === 'healthy' ? 'Healthy' : 'Degraded';
                    statusElement.className = `status-indicator status-${data.overall_status === 'healthy' ? 'healthy' : 'degraded'}`;

                    // Update system metrics
                    updateSystemMetrics(data.system);

                    // Update services
                    updateServices(data.service_details);

                    // Update performance
                    updatePerformance(data.performance);

                    // Update alerts
                    updateAlerts(data.alerts);

                    // Update timestamp
                    const timestamp = new Date(data.timestamp).toLocaleString();
                    document.getElementById('last-updated').textContent = `Last updated: ${timestamp}`;

                    lastUpdate = new Date();
                })
                .catch(error => {
                    console.error('Error fetching health data:', error);
                    document.getElementById('overall-status').textContent = 'Connection Error';
                    document.getElementById('overall-status').className = 'status-indicator status-error';
                });
        }

        function updateSystemMetrics(system) {
            const container = document.getElementById('system-metrics');

            const metrics = [
                { label: 'CPU Usage', value: system.cpu_percent, unit: '%' },
                { label: 'Memory Usage', value: system.memory_percent, unit: '%' },
                { label: 'Disk Usage', value: system.disk_percent, unit: '%' },
                { label: 'Processes', value: system.process_count, unit: '' }
            ];

            container.innerHTML = metrics.map(metric => {
                const isPercentage = metric.unit === '%';
                const progressClass = isPercentage ? getProgressClass(metric.value) : 'progress-normal';
                const progressWidth = isPercentage ? metric.value : 0;

                return `
                    <div class="metric">
                        <div>
                            <div class="metric-label">${metric.label}</div>
                            ${isPercentage ? `
                                <div class="progress-bar">
                                    <div class="progress-fill ${progressClass}" style="width: ${progressWidth}%"></div>
                                </div>
                            ` : ''}
                        </div>
                        <div class="metric-value">${metric.value}${metric.unit}</div>
                    </div>
                `;
            }).join('');
        }

        function updateServices(services) {
            const container = document.getElementById('services-status');

            container.innerHTML = services.map(service => {
                const statusClass = service.status === 'healthy' ? 'service-healthy' : 'service-unhealthy';
                const responseTime = service.response_time_ms ? `${service.response_time_ms.toFixed(0)}ms` : 'N/A';

                return `
                    <div class="service-item ${statusClass}">
                        <div>
                            <div class="metric-label">${service.service}</div>
                            <div style="font-size: 12px; color: #7f8c8d;">${responseTime}</div>
                        </div>
                        <div class="metric-value" style="color: ${service.status === 'healthy' ? '#27ae60' : '#e74c3c'}">
                            ${service.status.toUpperCase()}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function updatePerformance(performance) {
            const container = document.getElementById('performance-metrics');

            container.innerHTML = `
                <div class="metric">
                    <div class="metric-label">Average Response Time</div>
                    <div class="metric-value">${performance.avg_response_time_ms}ms</div>
                </div>
            `;
        }

        function updateAlerts(alerts) {
            const alertsSection = document.getElementById('alerts-section');
            const alertsList = document.getElementById('alerts-list');

            if (alerts && alerts.length > 0) {
                alertsSection.style.display = 'block';
                alertsList.innerHTML = alerts.map(alert =>
                    `<div class="alert-item">${alert}</div>`
                ).join('');
            } else {
                alertsSection.style.display = 'none';
            }
        }

        function getProgressClass(value) {
            if (value >= 90) return 'progress-critical';
            if (value >= 70) return 'progress-warning';
            return 'progress-normal';
        }

        // Update every 10 seconds
        updateStatus();
        setInterval(updateStatus, 10000);

        // Update page title with status
        setInterval(() => {
            const statusElement = document.getElementById('overall-status');
            if (statusElement) {
                const status = statusElement.textContent;
                document.title = `[${status}] Nutrition Intelligence Monitor`;
            }
        }, 1000);
    </script>
</body>
</html>'''

    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)

    print("Monitoring Dashboard starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)