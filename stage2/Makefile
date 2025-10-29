SHELL := /bin/bash

.PHONY: up down logs migrate upgrade refresh shell clear-cache

# Build and start containers
up:
	docker compose up --build -d

# Stop containers
down:
	docker compose down

# View logs live
logs:
	docker compose logs -f web

# Run DB migrations inside container
migrate:
	docker compose exec web flask db upgrade

upgrade:
	docker compose exec web flask db upgrade

# Run refresh operation
refresh:
	curl -X POST http://localhost:5000/countries/refresh

# Clear cache file
clear-cache:
	rm -f cache/summary.png
