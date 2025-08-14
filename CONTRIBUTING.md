# Contributing to SAGE Research Agent

Thank you for your interest in contributing to SAGE Research Agent! We welcome contributions from the community and are excited to work with you.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/raythurman2386/research-agent.git
   cd research-agent
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r enhanced_requirements.txt
   pip install pytest black flake8 mypy
   ```

## 🛠️ Development Process

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following our coding standards
3. **Write tests** for new functionality
4. **Run tests** to ensure everything works:
   ```bash
   pytest tests/
   ```
5. **Format your code**:
   ```bash
   black .
   flake8 .
   ```

### Commit Guidelines

- Use clear, descriptive commit messages
- Follow the format: `type(scope): description`
- Examples:
  - `feat(search): add academic search functionality`
  - `fix(cache): resolve database connection issue`
  - `docs(readme): update installation instructions`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_search.py

# Run with coverage
pytest --cov=sage_agent tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)
- Mock external API calls

Example:
```python
def test_web_search_returns_results():
    # Arrange
    query = "test query"
    expected_results = ["result1", "result2"]
    
    # Act
    results = web_search(query)
    
    # Assert
    assert isinstance(results, str)
    assert len(json.loads(results)) > 0
```

## 📝 Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [Flake8](https://flake8.pycqa.org/) for linting
- Use type hints where possible

### Documentation

- Write clear docstrings for all functions and classes
- Use Google-style docstrings
- Update README.md for new features
- Add inline comments for complex logic

Example:
```python
def web_search(query: str) -> str:
    """Performs a comprehensive web search to find information on a topic.
    
    Args:
        query: The search query string
        
    Returns:
        JSON string containing search results
        
    Raises:
        SearchError: If the search API is unavailable
    """
```

## 🐛 Bug Reports

### Before Submitting

- Check existing issues to avoid duplicates
- Try the latest version to see if the bug is fixed
- Gather relevant information about your environment

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Environment**
- OS: [e.g. Windows 11, macOS 13]
- Python version: [e.g. 3.9.0]
- SAGE version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

## 💡 Feature Requests

### Before Submitting

- Check if the feature already exists
- Review existing feature requests
- Consider if it fits the project's scope

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Explain how this feature would be used and why it's valuable.

**Proposed Implementation**
If you have ideas about how to implement this feature.

**Alternatives**
Any alternative solutions you've considered.
```

## 🏗️ Architecture Guidelines

### Adding New Tools

1. **Create the tool function** in `enhanced_sage_agent.py`
2. **Add comprehensive docstring** with args and return types
3. **Include error handling** with try-catch blocks
4. **Add the tool** to the agent's tool dictionary
5. **Update the system prompt** to include the new tool
6. **Write tests** for the new functionality

### Tool Function Template

```python
def new_tool(parameter: str) -> str:
    """Brief description of what the tool does.
    
    Args:
        parameter: Description of the parameter
        
    Returns:
        Description of what is returned
    """
    print(f"TOOL: Description of action being performed...")
    
    try:
        # Tool implementation
        result = perform_action(parameter)
        return result
    except Exception as e:
        return f"Error in new_tool: {e}"
```

## 📋 Pull Request Process

1. **Ensure your PR**:
   - Has a clear title and description
   - References any related issues
   - Includes tests for new functionality
   - Passes all existing tests
   - Follows our coding standards

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] All tests pass
   - [ ] New tests added for new functionality
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   ```

3. **Review Process**:
   - All PRs require at least one review
   - Address feedback promptly
   - Keep PRs focused and reasonably sized

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Communication

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for questions and general discussion
- Be patient and helpful when answering questions
- Search existing issues/discussions before creating new ones

## 🏆 Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- Annual contributor highlights

## 📞 Getting Help

- 📖 **Documentation**: Check the README and wiki first
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Create an issue for bugs or feature requests
- 📧 **Direct Contact**: For sensitive issues, email the maintainers

## 📈 Roadmap Contributions

We welcome contributions toward our roadmap items:

- **High Priority**: Multi-language support, API endpoints
- **Medium Priority**: Custom report templates, visualizations
- **Low Priority**: Web interface, real-time collaboration

Thank you for contributing to SAGE Research Agent! 🎉
