
.PHONY: format lint

all: format lint

format:
	uv run ruff format	

lint:
	uv run ruff check --fix 
	uv run ty check


