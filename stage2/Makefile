SHELL := /bin/bash

.PHONY: up down logs migrate upgrade refresh countries country delete image status restart shell clear-cache

# Build and start containers
up:
	docker compose up --build -d

# Stop containers
down:
	docker compose down

restart: down up

# View logs live
logs:
	docker compose logs -f web

# Run DB migrations inside container
migrate:
	docker compose exec web flask db upgrade

upgrade:
	docker compose exec web flask db upgrade

countries:
	curl -X GET http://localhost:5000/countries

country:
	curl -X GET http://localhost:5000/countries/$(COUNTRY)

delete:
	curl -X DELETE http://localhost:5000/countries/$(COUNTRY)

image:
	curl -X GET http://localhost:5000/countries/image

# Run refresh operation
refresh:
	curl -X POST http://localhost:5000/countries/refresh

# Run refresh operation
status:
	curl -X GET http://localhost:5000/status

# Clear cache file
clear-cache:
	rm -f cache/summary.png
