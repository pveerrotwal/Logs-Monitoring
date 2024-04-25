#!/bin/bash

#apache access_log file to monitor from my device
LOG_FILE="/opt/homebrew/var/log/httpd/access_log"

# Function to monitor log file
monitor_log_file() {
    trap 'echo "Monitoring interrupted. Exiting."; exit' INT
    tail -n 0 -F "$LOG_FILE" | while read line; do
        echo "$line"
    done
}

# Function for log analysis
analyze_log() {
    # Count occurrences of specific keywords or patterns
    echo "Analyzing log entries..."
    echo "Counting occurrences of error messages:"
    grep -c "ERROR" "$LOG_FILE"
    echo "Counting occurrences of HTTP status codes:"
    grep -c "HTTP" "$LOG_FILE"
    # Generate summary reports
    echo "Top error messages:"
    grep "ERROR" "$LOG_FILE" | sort | uniq -c | sort -rn | head -5
}

# Main function
main() {
    monitor_log_file &
    PID=$!
    analyze_log
    kill $PID
}

# Execute main function
main
