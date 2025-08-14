@echo off
REM Test runner script for Windows

if "%1"=="help" (
    echo Available commands:
    echo   test           - Run all tests
    echo   test-verbose   - Run tests with verbose output
    echo   test-coverage  - Run tests with coverage report
    echo   test-unit      - Run only unit tests
    echo   test-integration - Run only integration tests
    echo   test-debug     - Run tests with output capture disabled
    echo   test-file      - Run specific test file ^(provide filename^)
    echo   clean          - Clean test artifacts
    echo   install        - Install test dependencies
    echo   lint-test      - Run linting and tests
    goto :eof
)

if "%1"=="test" (
    uv run pytest
    goto :eof
)

if "%1"=="test-verbose" (
    uv run pytest -v
    goto :eof
)

if "%1"=="test-coverage" (
    uv run pytest --cov=. --cov-report=term-missing --cov-report=html
    goto :eof
)

if "%1"=="test-unit" (
    uv run pytest -m "not integration and not slow"
    goto :eof
)

if "%1"=="test-integration" (
    uv run pytest -m integration
    goto :eof
)

if "%1"=="test-debug" (
    uv run pytest -s
    goto :eof
)

if "%1"=="test-file" (
    if "%2"=="" (
        echo Please provide a test file name
        echo Example: test.bat test-file test_agent.py
    ) else (
        uv run pytest tests/%2 -v
    )
    goto :eof
)

if "%1"=="clean" (
    if exist htmlcov rmdir /s /q htmlcov
    if exist .pytest_cache rmdir /s /q .pytest_cache
    if exist .coverage del .coverage
    if exist pytest.xml del pytest.xml
    for /r %%i in (*.pyc) do del "%%i"
    for /d /r %%i in (__pycache__) do if exist "%%i" rmdir /s /q "%%i"
    echo Test artifacts cleaned
    goto :eof
)

if "%1"=="install" (
    uv add pytest pytest-mock pytest-cov
    goto :eof
)

if "%1"=="lint-test" (
    uv run ruff check
    uv run ruff format --check
    uv run pytest
    goto :eof
)

REM Default action - run all tests
if "%1"=="" (
    echo Running all tests...
    uv run pytest
) else (
    echo Unknown command: %1
    echo Use "test.bat help" for available commands
)
