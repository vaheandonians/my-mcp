# MY MCP

A template MCP (Model Context Protocol) server.

## Setup

### Environment Configuration

Create a `.env` file in the project root with the following contents:

```
SAMPLE_SECRET=your_password_here
```

### Dependencies Management

All dependencies are defined in `pyproject.toml` as the single source of truth. The `requirements.txt` file is automatically generated from it.

**Note:** You don't need to manually edit `requirements.txt` - it's auto-generated!

```bash
# Generate requirements.txt from pyproject.toml
make sync-requirements

# Or run the script directly
python scripts/sync-requirements.py
```

The build scripts automatically generate `requirements.txt` from `pyproject.toml` before building the Docker image, ensuring consistency between local development and containerized environments.

#### Adding New Dependencies

To add new dependencies:

1. Add them to `pyproject.toml` under `dependencies`
2. Run `uv sync` to update your local environment
3. Run `make sync-requirements` to update `requirements.txt`
4. Commit both `pyproject.toml` and `requirements.txt`

Example:
```bash
# Add a new dependency to pyproject.toml, then:
uv sync                    # Update local environment
make sync-requirements     # Update requirements.txt
```

**CI/CD Note:** While the Dockerfile generates `requirements.txt` automatically during build, we recommend committing the generated `requirements.txt` to the repository for:
- Faster Docker builds (better layer caching)
- Compatibility with systems that expect a requirements.txt file
- Clear visibility of exact dependencies

### Using uv (recommended):

#### 1. Install uv:

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

#### 2. Create virtual environment:

   ```
   uv venv
   ```

#### 3. Install dependencies:

   ```
   uv sync
   ```

#### 4. Install dependencies and package:

   ```
   uv pip install -e .
   ```

#### 5. Run tests:

   ```bash
   # Run all tests
   uv run pytest
   
   # Run specific test file
   uv run pytest tests/test_get_fibonacci_sequence.py -v
   ```

### Run the server:
   
   ```
   my-mcp-sse
   ```

   or

   ```
   my-mcp-stdio
   ```

## Docker

The Docker container packages the MCP server with all its dependencies and can run in either STDIO or SSE mode.

### Docker Image Features

- Based on Python 3.13 slim image for minimal size
- Uses pre-generated requirements.txt for faster builds
- Includes all required dependencies
- Stores secrets securely during build
- Automatically configures SSL certificates
- Supports both STDIO and SSE modes via entrypoint script
- Exposes port 8000 for SSE mode

### Building the Docker Image

#### Using the build script (recommended):

   ```bash
   ./build-docker-image.sh
   ```
   
   This script will:
   - Check for an existing `.env` file
   - Prompt for `SAMPLE_SECRET` if needed
   - Generate requirements.txt from pyproject.toml
   - Stop and remove any existing my-mcp containers
   - Build the Docker image with proper environment variables
   - Display usage instructions when complete

#### Manual Docker build:

   ```bash
   # First, generate requirements.txt
   python scripts/sync-requirements.py
   
   # Then build the Docker image
   docker build --build-arg SAMPLE_SECRET=your_secret_here -t my-mcp .
   ```

### Running the Docker Container

The Docker container supports two modes: STDIO and SSE (Server-Sent Events).

#### STDIO Mode (Default):

   ```bash
   # Interactive mode
   docker run -it my-mcp
   
   # Or explicitly specify stdio
   docker run -it my-mcp stdio
   ```

#### SSE Mode (Server-Sent Events):

   ```bash
   # Run on port 8000
   docker run -p 8000:8000 my-mcp sse
   
   # Run in background
   docker run -d -p 8000:8000 --name my-mcp-server my-mcp sse
   ```

**Note:** In SSE mode, the server automatically binds to `0.0.0.0` to allow connections from outside the Docker container.

#### Using Docker Compose:

Docker Compose provides an alternative way to build and run the container:

   ```bash
   # Build image and start SSE server
   docker-compose up -d --build
   
   # Start SSE server (uses existing image)
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop and remove containers
   docker-compose down
   ```

**Note:** Docker Compose reads `SAMPLE_SECRET` from your `.env` file automatically.

For more detailed Docker usage, see [docs/docker-usage.md](docs/docker-usage.md).

### Quick Commands

A Makefile is provided for common tasks:

```bash
# Sync requirements.txt from pyproject.toml
make sync-requirements

# Run tests
make test

# Build Docker image (includes sync-requirements)
make build-docker

# Run Docker in STDIO mode
make run-docker-stdio

# Run Docker in SSE mode
make run-docker-sse

# Docker Compose commands (alternative to direct Docker)
make compose-up    # Build and start services
make compose-down  # Stop and remove services
make compose-logs  # View service logs
```

## Development Workflow

### Project Structure

```
my-mcp/
├── pyproject.toml           # Project metadata and dependencies (source of truth)
├── requirements.txt         # Auto-generated from pyproject.toml
├── scripts/
│   └── sync-requirements.py # Script to generate requirements.txt
├── Dockerfile              # Multi-mode container with auto-generated requirements
├── Makefile               # Convenience commands
└── my_mcp/
    └── server.py          # Main MCP server implementation
```

### Common Development Tasks

```bash
# Install/update dependencies locally
uv sync

# Run tests
make test
# or
uv run pytest

# Update requirements.txt after changing pyproject.toml
make sync-requirements

# Build and run Docker
make build-docker
make run-docker-stdio  # or run-docker-sse
```

## Usage

Configure the MCP servers in your client by adding one of the following configurations:

### Local Installation

   ```json
   "my-mcp": {
      "command": "uv",
      "args": [
         "run",
         "/Users/vaheandonians/code/my-mcp/.venv/bin/my-mcp-stdio" 
      ]
   }
   ```

### Docker Container - STDIO Mode

For Claude Desktop App or other MCP clients:

   ```json
   "my-mcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "my-mcp", "stdio"]
   }
   ```

### Docker Container - SSE Mode

First, start the container in SSE mode:

   ```bash
   docker run -d -p 8000:8000 --name my-mcp-sse my-mcp sse
   ```

Then configure your MCP client to connect via SSE:

   ```json
   "my-mcp": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
   }
   ```

To manage the SSE container:

   ```bash
   # View logs
   docker logs -f my-mcp-sse
   
   # Stop the container
   docker stop my-mcp-sse
   
   # Remove the container
   docker rm my-mcp-sse
   ```