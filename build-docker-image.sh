#!/bin/bash

set -e

echo "=== My-MCP Docker Build Script ==="

# Check for .env file
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo ".env file not found. Creating a new one..."
    echo "Please enter the SAMPLE_SECRET value:"
    read -s sample_secret
    echo "SAMPLE_SECRET=$sample_secret" > "$ENV_FILE"
    echo ".env file created with SAMPLE_SECRET."
else
    echo ".env file found."
fi

# Source the .env file
set -a
source "$ENV_FILE"
set +a

# Validate required environment variables
if [ -z "$SAMPLE_SECRET" ]; then
    echo "Error: SAMPLE_SECRET is not set in .env file"
    exit 1
fi

echo "Stopping and removing existing my-mcp containers..."
docker ps -a --filter "name=my-mcp" -q | xargs -r docker rm -f || true

echo "Building new my-mcp Docker image..."
docker build --build-arg SAMPLE_SECRET="$SAMPLE_SECRET" -t my-mcp .

echo ""
echo "=== Build completed successfully! ==="
echo ""
echo "To run the container:"
echo "  STDIO mode:  docker run -i my-mcp"
echo "  SSE mode:    docker run -p 8000:8000 my-mcp sse"
echo ""
echo "Alternative: Use docker-compose for easier management:"
echo "  docker-compose up -d     # Runs SSE mode on port 8000"
echo ""
echo "For more options, see: docs/docker-usage.md" 