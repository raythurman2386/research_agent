# Testing Guide for Research Agent

This document provides comprehensive information about the testing setup for the SAGE Research Agent project.

## Overview

The project includes a comprehensive test suite using pytest with the following features:
- Unit tests for individual components
- Integration tests for end-to-end workflows
- Mocked external API calls to avoid real API usage during testing
- Coverage reporting
- Test categorization (unit, integration, slow tests)

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Test configuration and shared fixtures
├── test_agent.py              # Tests for basic SAGE agent
├── test_enhanced_agent.py     # Tests for enhanced SAGE agent
├── test_main.py               # Tests for main script functionality
└── test_integration.py        # Integration and performance tests
```

## Test Categories

### Unit Tests
- Test individual functions and classes in isolation
- Mock all external dependencies (APIs, databases, etc.)
- Fast execution (< 1 second per test)
- Located in: `test_agent.py`, `test_enhanced_agent.py`, `test_main.py`

### Integration Tests
- Test component interactions and workflows
- May use temporary databases or files
- Marked with `@pytest.mark.integration`
- Located in: `test_integration.py`

### Performance Tests
- Test performance characteristics and resource usage
- Marked with `@pytest.mark.slow`
- Located in: `test_integration.py` (TestPerformanceIntegration class)

## Key Test Components

### 1. Fixtures (conftest.py)
- `mock_api_keys`: Provides test API keys for Google and Tavily
- `mock_genai`: Mocks Google GenerativeAI calls
- `mock_tavily`: Mocks Tavily search client
- `temp_db`: Creates temporary SQLite database for testing
- `sample_research_goal`: Provides sample research topics
- `sample_search_results`: Provides sample search result data

### 2. Test Coverage Areas

#### Basic Agent Tests (`test_agent.py`)
- Web search functionality
- Reasoning tool operations
- Agent initialization and configuration
- Agent execution workflow
- Error handling
- Utility functions (filename generation, etc.)

#### Enhanced Agent Tests (`test_enhanced_agent.py`)
- Database operations (caching, persistence)
- Enhanced search tools (web, news, academic, market research)
- Analysis tools (data analysis, outline creation, quality checks)
- Research context management
- Advanced agent functionality

#### Main Script Tests (`test_main.py`)
- Environment validation
- Menu and display functions
- Agent runner functions
- Error handling
- Integration between components

#### Integration Tests (`test_integration.py`)
- End-to-end agent workflows
- Database persistence across operations
- Error handling in complex scenarios
- Performance characteristics

## Running Tests

### Prerequisites
```bash
# Install test dependencies
uv add pytest pytest-mock pytest-cov
```

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=. --cov-report=term-missing --cov-report=html
```

### Categorized Test Runs

```bash
# Run only unit tests (fast)
uv run pytest -m "not integration and not slow"

# Run only integration tests
uv run pytest -m integration

# Run only slow/performance tests
uv run pytest -m slow
```

### Specific Test Execution

```bash
# Run a specific test file
uv run pytest tests/test_agent.py -v

# Run a specific test class
uv run pytest tests/test_agent.py::TestSAGEAgent -v

# Run a specific test method
uv run pytest tests/test_agent.py::TestSAGEAgent::test_agent_initialization -v
```

### Windows Helper Scripts

For Windows users, convenience scripts are provided:

```batch
# Run all tests
test.bat

# Run with verbose output
test.bat test-verbose

# Run with coverage
test.bat test-coverage

# Run unit tests only
test.bat test-unit

# Clean test artifacts
test.bat clean
```

## Test Configuration

### pytest.ini
The project uses a `pytest.ini` configuration file with the following settings:
- Test discovery patterns
- Default command-line options
- Test markers for categorization
- Warning filters

### Coverage Configuration
Coverage reporting is configured to:
- Include all source files
- Exclude test files from coverage
- Generate both terminal and HTML reports
- Highlight missing coverage areas

## Mocking Strategy

### External APIs
All external API calls are mocked to:
- Avoid real API costs during testing
- Ensure tests run without internet connection
- Provide predictable test data
- Enable testing of error conditions

### Database Operations
Database operations use:
- Temporary SQLite files for isolation
- Automatic cleanup after tests
- Mock database connections where appropriate

### File System Operations
File operations use:
- Temporary directories and files
- Automatic cleanup
- Mock file operations for error testing

## Common Testing Patterns

### 1. Mocking External APIs
```python
def test_web_search_success(self, mock_tavily, mock_api_keys):
    """Test successful web search."""
    result = web_search("test query")
    assert "Test Article" in result
    mock_tavily.search.assert_called_once()
```

### 2. Testing Error Conditions
```python
def test_web_search_error(self, mock_api_keys):
    """Test web search with API error."""
    with patch("tavily.TavilyClient") as mock_client:
        mock_instance = Mock()
        mock_instance.search.side_effect = Exception("API Error")
        mock_client.return_value = mock_instance
        
        result = web_search("test query")
        assert "Error during search: API Error" in result
```

### 3. Database Testing
```python
def test_cache_search_result(self, temp_db):
    """Test caching search results."""
    db = ResearchDatabase(temp_db)
    db.cache_search_result("query", "results", "source")
    cached = db.get_cached_result("query")
    assert cached == "results"
```

## Test Data Management

### Sample Data
Tests use predefined sample data for consistency:
- Sample research goals
- Sample search results
- Sample API responses
- Sample file contents

### Test Isolation
Each test is isolated through:
- Fresh mock instances
- Temporary databases/files
- Clean environment variables
- No shared state between tests

## Continuous Integration

The test suite is designed to work in CI/CD environments:
- No external dependencies during tests
- Deterministic results
- XML output support for CI tools
- Coverage reporting for quality gates

```bash
# CI-friendly test run
uv run pytest --cov=. --cov-report=xml --junitxml=pytest.xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   uv sync
   ```

2. **API Key Warnings**: Tests should mock all API calls, check fixture usage

3. **Database Errors**: Temporary databases should be automatically cleaned up

4. **Path Issues**: Use absolute paths in test configurations

### Debug Mode
Run tests with output capture disabled to see debug information:
```bash
uv run pytest -s
```

### Test Specific Debugging
Add print statements or use pytest's debugging features:
```bash
uv run pytest --pdb  # Drop into debugger on failures
```

## Contributing to Tests

When adding new functionality:

1. **Write tests first** (TDD approach)
2. **Mock external dependencies** appropriately
3. **Use descriptive test names** that explain what is being tested
4. **Follow the existing test structure** and patterns
5. **Add integration tests** for complex workflows
6. **Update this documentation** if adding new test categories or patterns

### Test Naming Convention
- Test files: `test_<module_name>.py`
- Test classes: `Test<ComponentName>`
- Test methods: `test_<specific_behavior>`

### Example New Test
```python
def test_new_feature_success(self, mock_api_keys):
    """Test that new feature works correctly with valid input."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = new_feature(input_data)
    
    # Assert
    assert result == expected_output
    assert some_condition_is_true
```

This testing framework ensures the research agent components are reliable, maintainable, and ready for production use.
