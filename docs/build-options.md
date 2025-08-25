# Build Options

There are three ways to build and run the my-mcp Docker image:

## 1. Using build-docker-image.sh (Recommended for building)

```bash
./build-docker-image.sh
```

This script:
- Prompts for SAMPLE_SECRET if .env doesn't exist
- Sources .env file
- Builds the image with docker build
- Provides run instructions

## 2. Using docker-compose (Recommended for running)

```bash
# Build and run in one command
docker-compose up -d --build

# Or just run if image exists
docker-compose up -d
```

Docker Compose:
- Reads SAMPLE_SECRET from .env automatically
- Can build the image if needed
- Manages container lifecycle
- Better for production deployments

## 3. Manual docker commands

```bash
# Build
docker build --build-arg SAMPLE_SECRET="your-secret" -t my-mcp .

# Run
docker run -p 8000:8000 my-mcp sse
```

## Which to use?

- **Development**: Use `build-docker-image.sh` for interactive builds
- **Production**: Use `docker-compose` for deployment
- **CI/CD**: Use direct docker commands or docker-compose
