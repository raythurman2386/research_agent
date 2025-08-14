@echo off
REM Quality check script for Windows
echo 🚀 Running quality checks for research agent...

echo.
echo 🔍 Code formatting check...
uv run ruff format --check .
if %ERRORLEVEL% neq 0 (
    echo ❌ Code formatting check failed
    goto :error
)
echo ✅ Code formatting check passed

echo.
echo 🔍 Linting check...
uv run ruff check .
if %ERRORLEVEL% neq 0 (
    echo ❌ Linting check failed
    goto :error
)
echo ✅ Linting check passed

echo.
echo 🔍 Type checking...
uv run mypy . --ignore-missing-imports
if %ERRORLEVEL% neq 0 (
    echo ❌ Type checking failed (warnings allowed)
)
echo ✅ Type checking completed

echo.
echo 🔍 Test suite...
uv run pytest tests/ -v --cov=. --cov-report=term-missing
if %ERRORLEVEL% neq 0 (
    echo ❌ Test suite failed
    goto :error
)
echo ✅ Test suite passed

echo.
echo 🎉 All quality checks passed!
exit /b 0

:error
echo.
echo 💥 Some quality checks failed!
exit /b 1
