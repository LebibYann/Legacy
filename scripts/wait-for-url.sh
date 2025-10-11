#!/bin/bash
# Usage: ./wait-for-url.sh <URL> [timeout_seconds] [interval_seconds]
# Example: ./wait-for-url.sh http://localhost:2317 600 5

# Check for curl
if ! command -v curl > /dev/null 2>&1; then
  echo "❌ curl command not found. Please install curl."
  exit 1
fi

URL="$1"
TIMEOUT="${2:-600}"   # Default: 10 minutes
INTERVAL="${3:-5}"    # Default: 5 seconds
ELAPSED=0

if [ -z "$URL" ]; then
  echo "Usage: $0 <URL> [timeout_seconds] [interval_seconds]"
  exit 2
fi

echo "Waiting for $URL to respond..."
while [ $ELAPSED -lt $TIMEOUT ]; do
  if curl -s --connect-timeout 3 "$URL" > /dev/null 2>&1; then
    echo "$URL is ready!"
    exit 0
  fi
  echo "$URL not ready yet, waiting... ($ELAPSED/$TIMEOUT seconds)"
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "Timeout: $URL did not respond within $TIMEOUT seconds"
exit 1
