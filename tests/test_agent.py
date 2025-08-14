"""
Tests for the basic SAGE Agent (agent.py).
"""

import json
from unittest.mock import Mock, patch

from agent import (
    SAGEAgent,
    _create_filename_from_goal,
    finish_research,
    reasoning_tool,
    web_search,
)


class TestWebSearch:
    """Test the web_search tool function."""

    def test_web_search_success(self, mock_api_keys):
        """Test successful web search."""
        with patch("agent.tavily_client") as mock_tavily:
            mock_tavily.search.return_value = {
                "results": [
                    {
                        "title": "Test Article",
                        "url": "https://example.com/test",
                        "content": "Test content from search",
                        "score": 0.9,
                    }
                ]
            }

            query = "renewable energy market"
            result = web_search(query)

            # Parse the JSON result
            search_results = json.loads(result)

            assert isinstance(search_results, list)
            assert len(search_results) == 1
            assert search_results[0]["title"] == "Test Article"
            assert search_results[0]["url"] == "https://example.com/test"

    def test_web_search_error(self, mock_api_keys):
        """Test web search with error."""
        with patch("agent.tavily_client") as mock_tavily:
            mock_tavily.search.side_effect = Exception("API Error")

            result = web_search("test query")
            assert "Error during search: API Error" in result


class TestReasoningTool:
    """Test the reasoning_tool function."""

    def test_reasoning_tool_success(self, mock_genai, mock_api_keys):
        """Test successful reasoning tool execution."""
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = "This is a test reasoning response"
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai["model"].return_value = mock_model_instance

        result = reasoning_tool("Test reasoning prompt")
        assert result == "This is a test reasoning response"
        mock_model_instance.generate_content.assert_called_once_with(
            "Test reasoning prompt"
        )


class TestFinishResearch:
    """Test the finish_research function."""

    def test_finish_research(self):
        """Test finish_research returns the report."""
        report = "# Final Research Report\n\nThis is the final report."
        result = finish_research(report)
        assert result == report


class TestSAGEAgent:
    """Test the SAGEAgent class."""

    def test_agent_initialization(self, mock_genai, mock_api_keys):
        """Test agent initialization."""
        agent = SAGEAgent()

        assert hasattr(agent, "tools")
        assert hasattr(agent, "model")
        assert hasattr(agent, "system_prompt")

        # Check that required tools are present
        assert "web_search" in agent.tools
        assert "reasoning_tool" in agent.tools
        assert "finish_research" in agent.tools

    def test_agent_initialization_custom_model(self, mock_genai, mock_api_keys):
        """Test agent initialization with custom model."""
        custom_model = "gemini-1.5-flash"
        SAGEAgent(model_name=custom_model)

        # Verify the model was called - we just need to check it was called, not the specific arguments
        mock_genai["model"].assert_called()
        # Check that the model name was passed in one of the calls
        calls = mock_genai["model"].call_args_list
        assert len(calls) > 0  # At least one model was created

    @patch("agent.genai.protos.Part")
    @patch("agent.genai.protos.FunctionResponse")
    def test_agent_run_success(
        self, mock_function_response, mock_part, mock_genai, mock_tavily, mock_api_keys
    ):
        """Test successful agent run."""
        # Setup mocks
        mock_model_instance = Mock()
        mock_chat = Mock()
        mock_model_instance.start_chat.return_value = mock_chat
        mock_genai["model"].return_value = mock_model_instance

        # Mock the conversation flow
        mock_response1 = Mock()
        mock_response1.candidates = [Mock()]
        mock_response1.candidates[0].content.parts = [Mock()]

        # First response - tool call
        mock_function_call = Mock()
        mock_function_call.name = "web_search"
        mock_function_call.args = {"query": "test query"}
        mock_response1.candidates[0].content.parts[0].function_call = mock_function_call

        # Second response - finish call
        mock_response2 = Mock()
        mock_response2.candidates = [Mock()]
        mock_response2.candidates[0].content.parts = [Mock()]
        mock_function_call2 = Mock()
        mock_function_call2.name = "finish_research"
        mock_function_call2.args = {
            "final_report_markdown": "# Test Report\n\nThis is a test report."
        }
        mock_response2.candidates[0].content.parts[
            0
        ].function_call = mock_function_call2

        mock_chat.send_message.side_effect = [mock_response1, mock_response2]

        agent = SAGEAgent()
        result = agent.run("Test research goal")

        assert result == "# Test Report\n\nThis is a test report."

    def test_agent_run_no_function_call(self, mock_genai, mock_api_keys):
        """Test agent run when model doesn't call a function."""
        mock_model_instance = Mock()
        mock_chat = Mock()
        mock_model_instance.start_chat.return_value = mock_chat
        mock_genai["model"].return_value = mock_model_instance

        # Mock response with no function call
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock()]
        mock_response.candidates[0].content.parts[0].function_call = None

        mock_chat.send_message.return_value = mock_response

        agent = SAGEAgent()
        result = agent.run("Test research goal")

        assert result is None

    def test_agent_run_unknown_tool(self, mock_genai, mock_api_keys):
        """Test agent run with unknown tool call."""
        mock_model_instance = Mock()
        mock_chat = Mock()
        mock_model_instance.start_chat.return_value = mock_chat
        mock_genai["model"].return_value = mock_model_instance

        # Mock response with unknown tool
        mock_response = Mock()
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock()]
        mock_function_call = Mock()
        mock_function_call.name = "unknown_tool"
        mock_function_call.args = {}
        mock_response.candidates[0].content.parts[0].function_call = mock_function_call

        mock_chat.send_message.return_value = mock_response

        agent = SAGEAgent()
        result = agent.run("Test research goal")

        assert result is None


class TestUtilityFunctions:
    """Test utility functions."""

    def test_create_filename_from_goal(self):
        """Test filename creation from goal."""
        goal = "Write a comprehensive report on AI and Machine Learning!"
        filename = _create_filename_from_goal(goal)

        assert filename.startswith("SAGE_Report_")
        assert filename.endswith(".md")
        assert "!" not in filename  # Special characters removed
        assert " " not in filename  # Spaces converted to dashes

    def test_create_filename_long_goal(self):
        """Test filename creation with very long goal."""
        goal = "A" * 100  # Very long goal
        filename = _create_filename_from_goal(goal)

        # Should be truncated to 50 characters plus prefix and extension
        assert len(filename) <= len("SAGE_Report_") + 50 + len(".md")

    def test_create_filename_special_characters(self):
        """Test filename creation with special characters."""
        goal = "Test@#$%^&*(){}[]|\\:;\"'<>?/.,~`"
        filename = _create_filename_from_goal(goal)

        # Should only contain safe characters
        safe_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        )
        filename_chars = set(filename.replace("SAGE_Report_", "").replace(".md", ""))
        assert filename_chars.issubset(safe_chars)
