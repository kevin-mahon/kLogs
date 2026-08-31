# Python versions kLogs is expected to work on (3.10 -> 3.14).
PYTHON_VERSIONS := 3.10 3.11 3.12 3.13 3.14

.PHONY: all format lint test test-integration test-versions

all: format lint

format:
	uv run ruff format

lint:
	uv run ruff check --fix
	uv run ty check

# Unit tests. These run quickly, so
# run them often.
test:
	uv run pytest --cov=klogs \
	 --cov-report=term-missing tests/unit

# Integration tests. Run before each
# release.
test-integration:
	uv run pytest \
	 tests/unit tests/integration

# Run the unit tests against every supported
# Python version. Run before each release.
test-versions:
	@for v in $(PYTHON_VERSIONS); do \
		echo "=== Python $$v ==="; \
		uv python find $$v >/dev/null 2>&1 || uv python install $$v; \
		uv run --python $$v --isolated pytest tests/unit || exit 1; \
	done
