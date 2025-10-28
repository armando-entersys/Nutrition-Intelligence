#!/usr/bin/env python3
"""
Advanced Health Monitoring System for Nutrition Intelligence
Monitors system health, performance metrics, and service availability
"""
import asyncio
import psutil
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import aiohttp
import asyncpg
import redis.asyncio as redis

@dataclass
class HealthMetric:
    timestamp: str
    service: str
    status: str
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict] = None

@dataclass
class SystemMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict
    process_count: int
    load_average: List[float]

class HealthMonitor:
    def __init__(self, config: Dict):
        self.config = config
        self.services = config.get('services', {})
        self.metrics_history: List[HealthMetric] = []
        self.system_metrics_history: List[SystemMetrics] = []
        self.alert_thresholds = config.get('alert_thresholds', {})

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/health_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def check_http_service(self, name: str, url: str, timeout: int = 10) -> HealthMetric:
        """Check HTTP service health"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    response_time = (time.time() - start_time) * 1000

                    if response.status == 200:
                        return HealthMetric(
                            timestamp=datetime.now().isoformat(),
                            service=name,
                            status="healthy",
                            response_time_ms=response_time,
                            metadata={"status_code": response.status}
                        )
                    else:
                        return HealthMetric(
                            timestamp=datetime.now().isoformat(),
                            service=name,
                            status="unhealthy",
                            response_time_ms=response_time,
                            error_message=f"HTTP {response.status}",
                            metadata={"status_code": response.status}
                        )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                service=name,
                status="unhealthy",
                response_time_ms=response_time,
                error_message=str(e)
            )

    async def check_database(self, name: str, connection_string: str) -> HealthMetric:
        """Check PostgreSQL database health"""
        start_time = time.time()
        try:
            conn = await asyncpg.connect(connection_string)
            await conn.execute("SELECT 1")
            await conn.close()

            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                service=name,
                status="healthy",
                response_time_ms=response_time
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                service=name,
                status="unhealthy",
                response_time_ms=response_time,
                error_message=str(e)
            )

    async def check_redis(self, name: str, connection_string: str) -> HealthMetric:
        """Check Redis health"""
        start_time = time.time()
        try:
            r = redis.from_url(connection_string)
            await r.ping()
            await r.close()

            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                service=name,
                status="healthy",
                response_time_ms=response_time
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthMetric(
                timestamp=datetime.now().isoformat(),
                service=name,
                status="unhealthy",
                response_time_ms=response_time,
                error_message=str(e)
            )

    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent

        # Network I/O
        network = psutil.net_io_counters()
        network_io = {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }

        # Process count
        process_count = len(psutil.pids())

        # Load average (Unix-like systems)
        try:
            load_average = list(psutil.getloadavg())
        except AttributeError:
            # Windows doesn't have load average
            load_average = [0.0, 0.0, 0.0]

        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            network_io=network_io,
            process_count=process_count,
            load_average=load_average
        )

    async def run_health_checks(self) -> List[HealthMetric]:
        """Run all configured health checks"""
        tasks = []

        for service_name, service_config in self.services.items():
            service_type = service_config.get('type')

            if service_type == 'http':
                task = self.check_http_service(
                    service_name,
                    service_config['url'],
                    service_config.get('timeout', 10)
                )
                tasks.append(task)
            elif service_type == 'database':
                task = self.check_database(
                    service_name,
                    service_config['connection_string']
                )
                tasks.append(task)
            elif service_type == 'redis':
                task = self.check_redis(
                    service_name,
                    service_config['connection_string']
                )
                tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and log them
        health_metrics = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                service_name = list(self.services.keys())[i]
                self.logger.error(f"Health check failed for {service_name}: {result}")
                health_metrics.append(HealthMetric(
                    timestamp=datetime.now().isoformat(),
                    service=service_name,
                    status="error",
                    error_message=str(result)
                ))
            else:
                health_metrics.append(result)

        return health_metrics

    def check_alerts(self, metrics: List[HealthMetric], system_metrics: SystemMetrics):
        """Check if any metrics exceed alert thresholds"""
        alerts = []

        # Check service health alerts
        for metric in metrics:
            if metric.status != "healthy":
                alerts.append(f"🚨 Service {metric.service} is {metric.status}: {metric.error_message}")

            # Check response time alerts
            if metric.response_time_ms and metric.response_time_ms > self.alert_thresholds.get('response_time_ms', 5000):
                alerts.append(f"⚠️ Service {metric.service} response time is high: {metric.response_time_ms:.2f}ms")

        # Check system resource alerts
        if system_metrics.cpu_percent > self.alert_thresholds.get('cpu_percent', 80):
            alerts.append(f"🚨 High CPU usage: {system_metrics.cpu_percent:.1f}%")

        if system_metrics.memory_percent > self.alert_thresholds.get('memory_percent', 80):
            alerts.append(f"🚨 High memory usage: {system_metrics.memory_percent:.1f}%")

        if system_metrics.disk_percent > self.alert_thresholds.get('disk_percent', 90):
            alerts.append(f"🚨 High disk usage: {system_metrics.disk_percent:.1f}%")

        return alerts

    def generate_report(self, metrics: List[HealthMetric], system_metrics: SystemMetrics) -> Dict:
        """Generate comprehensive health report"""
        healthy_services = [m for m in metrics if m.status == "healthy"]
        unhealthy_services = [m for m in metrics if m.status != "healthy"]

        avg_response_time = 0
        if healthy_services:
            response_times = [m.response_time_ms for m in healthy_services if m.response_time_ms]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)

        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy" if len(unhealthy_services) == 0 else "degraded",
            "services": {
                "total": len(metrics),
                "healthy": len(healthy_services),
                "unhealthy": len(unhealthy_services)
            },
            "performance": {
                "avg_response_time_ms": round(avg_response_time, 2)
            },
            "system": asdict(system_metrics),
            "service_details": [asdict(m) for m in metrics],
            "alerts": self.check_alerts(metrics, system_metrics)
        }

    async def monitor_loop(self, interval: int = 60):
        """Main monitoring loop"""
        self.logger.info("Starting health monitoring loop...")

        while True:
            try:
                # Run health checks
                health_metrics = await self.run_health_checks()
                self.metrics_history.extend(health_metrics)

                # Collect system metrics
                system_metrics = self.collect_system_metrics()
                self.system_metrics_history.append(system_metrics)

                # Generate report
                report = self.generate_report(health_metrics, system_metrics)

                # Log summary
                self.logger.info(f"Health check completed - Status: {report['overall_status']}, "
                               f"Services: {report['services']['healthy']}/{report['services']['total']} healthy, "
                               f"Avg response time: {report['performance']['avg_response_time_ms']}ms")

                # Log alerts
                for alert in report['alerts']:
                    self.logger.warning(alert)

                # Save report to file
                with open(f"logs/health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                    json.dump(report, f, indent=2)

                # Clean up old metrics (keep last 24 hours)
                cutoff = datetime.now() - timedelta(hours=24)
                cutoff_str = cutoff.isoformat()

                self.metrics_history = [m for m in self.metrics_history if m.timestamp > cutoff_str]
                self.system_metrics_history = [m for m in self.system_metrics_history if m.timestamp > cutoff_str]

                await asyncio.sleep(interval)

            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(interval)

async def main():
    """Main function to run health monitoring"""
    # Configuration
    config = {
        'services': {
            'frontend': {
                'type': 'http',
                'url': 'http://localhost:3005/health',
                'timeout': 10
            },
            'backend': {
                'type': 'http',
                'url': 'http://localhost:8001/health',
                'timeout': 10
            },
            'api_foods': {
                'type': 'http',
                'url': 'http://localhost:8001/api/v1/foods',
                'timeout': 10
            }
        },
        'alert_thresholds': {
            'response_time_ms': 5000,
            'cpu_percent': 80,
            'memory_percent': 80,
            'disk_percent': 90
        }
    }

    # Create logs directory
    import os
    os.makedirs('logs', exist_ok=True)

    # Initialize and start monitor
    monitor = HealthMonitor(config)
    await monitor.monitor_loop(interval=30)  # Check every 30 seconds

if __name__ == "__main__":
    asyncio.run(main())