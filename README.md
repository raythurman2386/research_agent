# 🎯 SAGE Research Agent

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blue.svg)](https://ai.google.dev/)

**S**elf-**A**daptive, **G**oal-**O**riented AI Research Agent for comprehensive research automation and intelligent report generation.

## 🌟 Overview

SAGE is an advanced AI research agent that autonomously conducts comprehensive research on any topic, synthesizes information from multiple sources, and generates professional-quality reports. Built on Google's Gemini AI, SAGE combines web search capabilities, academic research, market analysis, and intelligent data synthesis to deliver publication-ready research reports.

### ✨ Key Features

- 🔍 **Multi-Source Research**: Web search, news, academic papers, and market research
- 🧠 **AI-Powered Analysis**: Intelligent data synthesis and trend analysis
- 📊 **Quality Assessment**: Built-in quality checking and iterative improvement
- 💾 **Smart Caching**: SQLite database for efficient search result caching
- 📝 **Intelligent Naming**: Automatic generation of descriptive, timestamped filenames
- 🎯 **Goal-Oriented**: Self-adaptive research process with progress tracking
- 📈 **Professional Output**: Publication-ready markdown reports with proper structure

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Generative AI API key
- Tavily Search API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/sage-research-agent.git
   cd sage-research-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r enhanced_requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_generative_ai_api_key
   TAVILY_API_KEY=your_tavily_search_api_key
   ```

4. **Run your first research:**
   ```bash
   python enhanced_sage_agent.py
   ```

## 📋 Usage

### Basic Usage

```python
from enhanced_sage_agent import EnhancedSAGEAgent

# Initialize the agent
agent = EnhancedSAGEAgent()

# Define your research goal
research_goal = """
Write a comprehensive report on renewable energy market trends, 
including growth projections, key technologies, and investment patterns.
"""

# Run the research
final_report = agent.run(goal=research_goal, max_iterations=25)

# Report is automatically saved with an intelligent filename
```

### Customizing Research Parameters

```python
# Custom configuration
agent = EnhancedSAGEAgent(model_name="gemini-1.5-pro-latest")

# Run with specific parameters
report = agent.run(
    goal="Your research topic",
    max_iterations=30  # Adjust based on research complexity
)
```

## 🛠️ Architecture

### Research Process Flow

```
1. Planning Phase
   ├── Generate research outline
   ├── Identify key research questions
   └── Define success criteria

2. Gathering Phase
   ├── General web search
   ├── News and current events
   ├── Academic and scholarly sources
   └── Market research reports

3. Analysis Phase
   ├── Data synthesis and analysis
   ├── Trend identification
   └── Pattern recognition

4. Quality Assessment
   ├── Completeness evaluation
   ├── Accuracy verification
   └── Gap identification

5. Iteration & Refinement
   ├── Address identified gaps
   ├── Enhance weak areas
   └── Validate findings

6. Finalization
   ├── Intelligent filename generation
   ├── Professional report formatting
   └── Metadata inclusion
```

### Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `web_search` | General web search | Broad topic exploration |
| `news_search` | Recent news articles | Current events and trends |
| `academic_search` | Scholarly papers | Research-backed insights |
| `market_research` | Industry reports | Market analysis and data |
| `analyze_data` | Data synthesis | Pattern identification |
| `create_outline` | Research planning | Structured approach |
| `quality_check` | Content assessment | Iterative improvement |

## 📊 Output Examples

### Intelligent Filename Generation

SAGE automatically generates descriptive, professional filenames:

- `Renewable-Energy-Market-Analysis_20250814_143022.md`
- `AI-Industry-Trends-Report_20250814_151205.md`
- `Cryptocurrency-Investment-Landscape_20250814_162847.md`

### Report Structure

```markdown
# Topic Analysis Report

## Executive Summary
Comprehensive overview of findings...

## Market Size and Growth
Detailed market analysis...

## Competitive Landscape
Key players and market dynamics...

## Emerging Technologies
Latest innovations and trends...

## Future Outlook (2025-2030)
Projections and recommendations...
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Generative AI API key | ✅ |
| `TAVILY_API_KEY` | Tavily Search API key | ✅ |

### Advanced Configuration

```python
# Customize model and settings
agent = EnhancedSAGEAgent(
    model_name="gemini-1.5-pro-latest"
)

# Access research context for monitoring
print(f"Sources consulted: {len(agent.context.sources)}")
print(f"Research phase: {agent.context.current_phase}")
```

## 📈 Performance Metrics

- **⚡ Speed**: Typical research completion in 1-3 minutes
- **🎯 Efficiency**: Average 8-12 iterations for comprehensive reports
- **📚 Source Diversity**: 4+ different search types per research session
- **✅ Quality**: Built-in assessment ensures report completeness

## 🧪 Testing

SAGE includes a comprehensive test suite with 57 tests covering all major components:

### Quick Test Setup
```bash
# Install test dependencies
uv add pytest pytest-mock pytest-cov

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=html
```

### Windows Users
```batch
# Use the provided batch script
test.bat
test.bat test-coverage
test.bat test-unit
```

### Test Categories
- **Unit Tests**: Individual component testing (fast)
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Resource usage and timing tests

### Coverage Areas
- ✅ Basic Agent functionality
- ✅ Enhanced Agent features
- ✅ Database operations
- ✅ Error handling
- ✅ API integrations (mocked)
- ✅ File operations

For detailed testing information, see:
- **Quick Start**: [TEST_QUICKSTART.md](docs/TEST_QUICKSTART.md)
- **Comprehensive Guide**: [TESTING.md](docs/TESTING.md)

## 🗃️ Data Management

### Research Cache

SAGE uses SQLite for intelligent caching:

```sql
-- Cached search results
CREATE TABLE search_cache (
    query TEXT PRIMARY KEY,
    results TEXT,
    timestamp DATETIME,
    source TEXT
);

-- Research session history
CREATE TABLE research_sessions (
    session_id TEXT PRIMARY KEY,
    goal TEXT,
    start_time DATETIME,
    end_time DATETIME,
    status TEXT,
    final_report TEXT
);
```

### Cache Benefits

- 🚀 **Faster Searches**: Avoid duplicate API calls
- 💰 **Cost Efficiency**: Reduce API usage costs
- 📊 **Research History**: Track past research sessions
- 🔄 **Reproducibility**: Consistent results for similar queries

## 🛡️ Error Handling

SAGE includes robust error handling:

- **Graceful Degradation**: Continues research if individual tools fail
- **Retry Logic**: Automatic retry for transient failures
- **Fallback Strategies**: Alternative approaches when primary methods fail
- **Comprehensive Logging**: Detailed error reporting and debugging

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_agent.py -v
```

### Code Quality

```bash
# Check code formatting
uv run ruff format --check .

# Auto-fix formatting issues
uv run ruff format .

# Run linting
uv run ruff check .

# Fix auto-fixable linting issues
uv run ruff check . --fix

# Run type checking
uv run mypy . --ignore-missing-imports
```

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### Workflows

- **🧪 Tests**: Runs on Python 3.11 and 3.12 with comprehensive test coverage
- **🎨 Code Quality**: Enforces formatting standards with ruff and type checking with mypy
- **📦 Build Check**: Verifies package builds successfully

### Status Badges

![Tests](https://github.com/raythurman2386/research-agent/actions/workflows/ci.yml/badge.svg)
![Code Quality](https://github.com/raythurman2386/research-agent/actions/workflows/code-quality.yml/badge.svg)

### Automated Checks

All pull requests are automatically validated for:
- ✅ Code formatting (ruff)
- ✅ Linting compliance (ruff check)
- ✅ Type safety (mypy)
- ✅ Test coverage (pytest)
- ✅ Cross-platform compatibility (Linux, Python 3.11-3.12)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Generative AI**: Powering the core intelligence
- **Tavily**: Providing comprehensive search capabilities
- **Open Source Community**: For the foundational libraries and tools

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/raythurman2386/research-agent/issues)

<div align="center">

**Built with ❤️ for researchers, analysts, and curious minds everywhere**

</div>
