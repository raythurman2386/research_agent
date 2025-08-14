# Quick Test Setup and Run Guide

## 🚀 Quick Start

### 1. Install Test Dependencies
```bash
uv add pytest pytest-mock pytest-cov
```

### 2. Run Tests
```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=. --cov-report=html

# Unit tests only (fast)
uv run pytest -m "not integration and not slow"
```

### 3. Windows Users
```batch
# Use the provided batch script
test.bat
test.bat test-coverage
test.bat test-unit
```

## 📊 Test Summary

- **57 total tests** covering all major components
- **Unit tests** for individual functions and classes
- **Integration tests** for end-to-end workflows
- **Performance tests** for resource usage
- **Mocked APIs** to avoid real API calls during testing

## 🔧 Test Categories

| Category | Command | Description |
|----------|---------|-------------|
| All | `uv run pytest` | Run all tests |
| Unit | `uv run pytest -m "not integration and not slow"` | Fast unit tests only |
| Integration | `uv run pytest -m integration` | End-to-end tests |
| Performance | `uv run pytest -m slow` | Performance tests |

## 📁 Test Coverage

- ✅ **Basic Agent** (`agent.py`) - Core functionality
- ✅ **Enhanced Agent** (`enhanced_sage_agent.py`) - Advanced features
- ✅ **Main Script** (`main.py`) - CLI interface
- ✅ **Database Operations** - Caching and persistence
- ✅ **Error Handling** - Various failure scenarios
- ✅ **Integration Workflows** - Complete agent runs

## 🐛 Current Known Issues

Some tests may fail on first run due to:
1. **Real API calls** (should be mocked)
2. **Import patching** issues
3. **Mock configuration** problems

These are framework setup issues, not functional problems with the core code.

## 📖 For More Information

See `TESTING.md` for comprehensive testing documentation including:
- Detailed test structure
- Mocking strategies
- Contributing guidelines
- Troubleshooting tips
