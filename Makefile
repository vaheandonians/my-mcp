.PHONY: sync-requirements test build-docker run-docker-stdio run-docker-sse

# Sync requirements.txt from pyproject.toml
sync-requirements:
	@echo "Syncing requirements.txt from pyproject.toml..."
	@python scripts/sync-requirements.py

# Run tests
test:
	uv run pytest

# Build Docker image
build-docker: sync-requirements
	./build-docker-image.sh

# Run Docker in STDIO mode
run-docker-stdio:
	docker run -it --rm my-mcp stdio

# Run Docker in SSE mode
run-docker-sse:
	docker run -d -p 8000:8000 --name my-mcp-sse my-mcp sse
	@echo "SSE server started on http://localhost:8000"
	@echo "View logs: docker logs -f my-mcp-sse"
	@echo "Stop server: docker stop my-mcp-sse && docker rm my-mcp-sse"

# Docker Compose commands
compose-up:
	docker-compose up -d --build
	@echo "Services started. View logs: docker-compose logs -f"

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f
