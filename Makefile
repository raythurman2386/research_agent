# Test Commands for Research Agent

# Run all tests
test:
	uv run pytest

# Run tests with verbose output
test-verbose:
	uv run pytest -v

# Run tests with coverage
test-coverage:
	uv run pytest --cov=. --cov-report=term-missing --cov-report=html

# Run only unit tests (excluding integration and slow tests)
test-unit:
	uv run pytest -m "not integration and not slow"

# Run only integration tests
test-integration:
	uv run pytest -m integration

# Run tests with output capture disabled (to see print statements)
test-debug:
	uv run pytest -s

# Run a specific test file
test-file:
	uv run pytest tests/test_agent.py -v

# Run tests and generate XML report for CI/CD
test-ci:
	uv run pytest --cov=. --cov-report=xml --junitxml=pytest.xml

# Clean test artifacts
clean-test:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -f .coverage
	rm -f pytest.xml
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Install test dependencies
install-test-deps:
	uv add pytest pytest-mock pytest-cov

# Run linting before tests
lint-and-test:
	uv run ruff check
	uv run ruff format --check
	uv run pytest

.PHONY: test test-verbose test-coverage test-unit test-integration test-debug test-file test-ci clean-test install-test-deps lint-and-test
