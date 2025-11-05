# ===============================
# 🌍 Eco-Mind — A2A Telex Agent
# ===============================

# -------- VARIABLES --------
APP_NAME=eco-mind
COMPOSE_FILE=docker-compose.yml
VENV_DIR=.venv

SERVICE ?= api

# Load environment variables from .env (so Docker + ngrok use same settings)
include .env
export $(shell sed 's/=.*//' .env)

# -------- TARGETS --------

help:
	@echo ""
	@echo "Eco-Mind CLI Commands"
	@echo "---------------------"
	@echo "make install          - Create venv & install deps"
	@echo "make run              - Run FastAPI locally (uvicorn)"
	@echo "make up       		 - Run full stack (API + Redis)"
	@echo "make down     		 - Stop and remove stack"
	@echo "make logs     		 - Tail logs for all services"
	@echo "make build     		 - Build only API Docker image"
	@echo "make attach			 - Attach to a running container"
	@echo "make debug            - Start container in DEBUG mode (interactive shell)"
	@echo "make ngrok            - Expose app publicly via ngrok"
	@echo "make clean            - Remove cache and pyc files"
	@echo ""

# -------- HELPER --------
# Checks for .venv, creates it if missing
define ensure_venv
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Creating one..."; \
		make install; \
	fi
endef

# ---- Local development ----
.PHONY: install
install:
	@echo "Setting up virtual environment..."
	python -m venv .venv
	@echo "Installing dependencies..."
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Virtual environment ready!"

# ---- Docker Compose Commands ----
.PHONY: up
up:
	docker compose -f $(COMPOSE_FILE) up --build -d

.PHONY: down
down:
	docker compose -f $(COMPOSE_FILE) down

.PHONY: logs
logs:
	docker compose -f $(COMPOSE_FILE) logs -f $(SERVICE)

# ---- Build image only ----
.PHONY: build
build:
	docker build -t $(APP_NAME):latest .

# ---- Attach to running container ----
.PHONY: attach
attach:
	docker compose exec api /bin/sh

# ---- Debug shell (interactive mode) ----
.PHONY: debug
debug:
	APP_ENV=debug docker compose run --rm api

# ---- Expose via ngrok ----
.PHONY: ngrok
ngrok:
	$(call ensure_venv)
	@echo "Starting ngrok tunnel on port 8000..."
	ngrok http 8800

# ---- Clean cache ----
.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache .venv
	find . -name "*.pyc" -delete

.PHONY: prune
prune:
	docker system prune -af --volumes
