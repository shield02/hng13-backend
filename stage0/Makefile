ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

APP_NAME ?= flask-cat-api
PORT ?= 5000
PYTHON ?= python3
VENV_DIR ?= .venv

.PHONY: help check-env setup install run test deploy clean

help:
	@echo "Available commands:"
	@echo "  make setup     - Create .env, venv, and install dependencies"
	@echo "  make install   - Install dependencies only"
	@echo "  make run       - Run the Flask app locally"
	@echo "  make test      - Run all tests"
	@echo "  make deploy    - Deploy app to Heroku"
	@echo "  make clean     - Remove temporary files"


# === Ensure .env exists ===
check-env:
	@if [ ! -f .env ]; then \
		echo ".env file not found — creating default one..."; \
		echo "FLASK_APP=app.py" > .env; \
		echo "FLASK_ENV=development" >> .env; \
		echo "PORT=5000" >> .env; \
		echo "HEROKU_APP_NAME=$(APP_NAME)" >> .env; \
		echo "Created default .env"; \
	else \
		echo ".env file found"; \
	fi

setup: check-env
	@echo "Setting up project environment..."
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Creating virtual environment at $(VENV_DIR)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "Installing dependencies..."
	@if [ ! -f requirements.txt ]; then \
		echo "Creating default requirements.txt..."; \
		echo "flask\nrequests\npytest\npython-dotenv" > requirements.txt; \
	fi
	@. $(VENV_DIR)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "Setup complete. To activate manually: source $(VENV_DIR)/bin/activate"

install: check-env
	@echo "Installing dependencies..."
	@if [ ! -f requirements.txt ]; then \
		echo "Creating default requirements.txt..."; \
		echo "flask\nrequests\npytest\npython-dotenv" > requirements.txt; \
	fi
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@echo "Dependencies installed."

run: check-env
	@echo "Running Flask app on port $${PORT:-5000}..."
	@python app/app.py

test: check-env
	@echo "Running tests..."
	@pytest -v

deploy: check-env
	@echo "Deploying $(APP_NAME) to Heroku..."
	@if [ -z "$(HEROKU_APP_NAME)" ]; then \
		echo "Error: HEROKU_APP_NAME not set in .env"; \
		exit 1; \
	fi
	@git add .
	@git commit -m "Deploying to Heroku" || true
	@git push https://git.heroku.com/$(HEROKU_APP_NAME).git HEAD:main
	@echo "Deployment complete!"

clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Clean complete."
