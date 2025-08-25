# Docker Usage Guide

This guide explains how to build and run the my-mcp server using Docker.

## Building the Docker Image

```bash
# Build with the sample secret
docker build --build-arg SAMPLE_SECRET="your-secret-value" -t my-mcp .

# Or use the build script
./build-docker-image.sh
```

## Running the Container

### STDIO Mode (Default)

STDIO mode is used for direct communication with the MCP client:

```bash
# Run in STDIO mode (default)
docker run -i my-mcp

# Or explicitly specify stdio
docker run -i my-mcp stdio
```

### SSE Mode (Server-Sent Events)

SSE mode runs an HTTP server on port 8000:

```bash
# Run in SSE mode
docker run -p 8000:8000 my-mcp sse

# Run in background
docker run -d -p 8000:8000 --name my-mcp-server my-mcp sse

# View logs
docker logs my-mcp-server
```

## Environment Variables

The container automatically sets:
- `SAMPLE_SECRET`: Read from the secret file created during build
- `SSL_CERT_FILE`: Points to the certifi certificate bundle

## Healthcheck

The container includes a healthcheck for SSE mode that verifies the server is responding on port 8000.

## Examples

### Interactive STDIO session
```bash
docker run -it my-mcp stdio
```

### Production SSE deployment
```bash
docker run -d \
  --name my-mcp-production \
  --restart unless-stopped \
  -p 8000:8000 \
  my-mcp sse
```

### Using with docker-compose

```yaml
version: '3.8'
services:
  my-mcp:
    build:
      context: .
      args:
        SAMPLE_SECRET: ${SAMPLE_SECRET}
    ports:
      - "8000:8000"
    command: sse
    restart: unless-stopped
```
