"""
Test script for logging system
Run this to verify logging configuration is working correctly
"""
import sys
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from core.logging import log_info, log_success, log_warning, log_error, logger

def test_basic_logging():
    """Test basic logging functions"""
    print("\n=== Testing Basic Logging ===\n")

    log_info("Testing info log")
    time.sleep(0.1)

    log_success("Testing success log")
    time.sleep(0.1)

    log_warning("Testing warning log")
    time.sleep(0.1)

    try:
        # Intentionally raise an error
        raise ValueError("Test error for logging")
    except Exception as e:
        log_error("Testing error log", error=e)

    print("\n✓ Basic logging tests completed")

def test_contextual_logging():
    """Test logging with context"""
    print("\n=== Testing Contextual Logging ===\n")

    log_info(
        "User action logged",
        request_id="test-request-123",
        user_id="user-456",
        business_context={
            "action": "test_logging",
            "module": "test_script"
        }
    )

    log_success(
        "Operation completed",
        request_id="test-request-123",
        user_id="user-456",
        business_context={
            "action": "test_complete",
            "duration_ms": 150
        }
    )

    log_warning(
        "Test warning with context",
        business_context={
            "warning_type": "test",
            "severity": "low"
        }
    )

    print("\n✓ Contextual logging tests completed")

def test_log_files():
    """Verify log files are created"""
    print("\n=== Checking Log Files ===\n")

    import os
    log_dir = Path("logs") if os.getenv("ENVIRONMENT") != "production" else Path("/app/logs")

    expected_files = ["app.log", "error.log", "access.log"]

    for log_file in expected_files:
        file_path = log_dir / log_file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✓ {log_file} exists ({size} bytes)")
        else:
            print(f"✗ {log_file} not found")

    print("\n✓ Log file check completed")

def test_json_format():
    """Test JSON log format"""
    print("\n=== Testing JSON Format ===\n")

    log_info(
        "JSON format test",
        request_id="json-test-123",
        business_context={
            "test": True,
            "nested": {
                "value": 42,
                "array": [1, 2, 3]
            }
        }
    )

    print("✓ JSON format test completed")
    print("  Check logs/app.log for JSON-formatted output")

def test_performance():
    """Test logging performance"""
    print("\n=== Testing Performance ===\n")

    iterations = 1000
    start_time = time.time()

    for i in range(iterations):
        log_info(f"Performance test iteration {i}", business_context={"iteration": i})

    duration = time.time() - start_time
    avg_time = (duration / iterations) * 1000  # ms

    print(f"✓ Logged {iterations} entries in {duration:.2f}s")
    print(f"  Average: {avg_time:.2f}ms per log entry")

    if avg_time < 5:
        print("  Performance: Excellent")
    elif avg_time < 10:
        print("  Performance: Good")
    else:
        print("  Performance: Needs optimization")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LOGGING SYSTEM TEST SUITE")
    print("="*60)

    try:
        test_basic_logging()
        test_contextual_logging()
        test_json_format()
        test_log_files()
        test_performance()

        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nNext steps:")
        print("1. Check logs/app.log for all log entries")
        print("2. Check logs/error.log for error entries only")
        print("3. Verify JSON format is correctly structured")
        print("4. Test log rotation by creating large log files")
        print("\n")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
