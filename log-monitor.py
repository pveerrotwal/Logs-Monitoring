import logging
import time
import signal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to monitor log file
def monitor_log_file(log_file):
    try:
        with open(log_file, 'r') as f:
            while True:
                new_line = f.readline()
                if new_line:
                    print(new_line.strip())
                else:
                    time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Monitoring interrupted.")
    except FileNotFoundError:
        logger.error(f"Log file '{log_file}' not found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Function for log analysis
def analyze_log(log_file):
    # Count occurrences of specific keywords or patterns
    print("Analyzing log entries...")
    with open(log_file, 'r') as f:
        error_count = sum(1 for line in f if 'ERROR' in line)
        http_count = sum(1 for line in f if 'HTTP' in line)
    print(f"Count of error messages: {error_count}")
    print(f"Count of HTTP status codes: {http_count}")
    # Generate summary reports
    print("Top error messages:")
    with open(log_file, 'r') as f:
        error_messages = [line.strip() for line in f if 'ERROR' in line]
    from collections import Counter
    top_errors = Counter(error_messages).most_common(5)
    for error, count in top_errors:
        print(f"{count}: {error}")

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\nMonitoring interrupted. Exiting.")
    exit(0)

if __name__ == "__main__":
    log_file = "/opt/homebrew/var/log/httpd/access_log" #apache access_log file to monitor
    try:
        # Start log monitoring
        signal.signal(signal.SIGINT, signal_handler)
        monitor_log_file(log_file)
        # Perform log analysis
        analyze_log(log_file)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
