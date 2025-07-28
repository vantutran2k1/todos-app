# Project Makefile

.PHONY: help run migrate makemigrations upgrade

# Load env if needed
ENV_FILE=.env

# Default values
APP=app.main:app
HOST=127.0.0.1
PORT=8000
WORKERS=1

help:
	@echo "Available commands:"
	@echo "  make run             - Start the FastAPI app with uvicorn"
	@echo "  make makemigrations  - Create a new Alembic migration"
	@echo "  make migrate         - Apply all pending Alembic migrations"
	@echo "  make revision NAME= - Create revision with message"

run:
	uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

makemigrations:
	alembic revision --autogenerate -m "$(NAME)"

migrate:
	alembic upgrade head

# Optional: downgrade migration by 1 step
downgrade:
	alembic downgrade -1
