"""
Tests for the main script (main.py).
"""

import os
from unittest.mock import Mock, patch

from main import (
    check_environment,
    display_header,
    display_menu,
    get_predefined_topics,
    run_basic_agent,
    run_enhanced_agent,
)


class TestEnvironmentChecks:
    """Test environment validation functions."""

    def test_check_environment_both_keys_present(self):
        """Test environment check when both API keys are present."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "test-google-key",
                "TAVILY_API_KEY": "test-tavily-key",
            },
        ):
            result = check_environment()
            assert result is True

    def test_check_environment_missing_google_key(self):
        """Test environment check when Google API key is missing."""
        with patch.dict(os.environ, {"TAVILY_API_KEY": "test-tavily-key"}, clear=True):
            with patch("builtins.print") as mock_print:
                result = check_environment()
                assert result is False
                # Check that appropriate error message was printed
                mock_print.assert_any_call(
                    "❌ GOOGLE_API_KEY not found in environment variables"
                )

    def test_check_environment_missing_tavily_key(self):
        """Test environment check when Tavily API key is missing."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-google-key"}, clear=True):
            with patch("builtins.print") as mock_print:
                result = check_environment()
                assert result is False
                # Check that appropriate error message was printed
                mock_print.assert_any_call(
                    "❌ TAVILY_API_KEY not found in environment variables"
                )

    def test_check_environment_no_keys(self):
        """Test environment check when no API keys are present."""

        # Mock each specific environment variable call
        def mock_getenv(key, default=None):
            return None  # Always return None for missing keys

        with patch("main.os.getenv", side_effect=mock_getenv):
            with patch("builtins.print") as mock_print:
                result = check_environment()
                assert result is False
                # Check that at least one error message was printed about missing keys
                printed_calls = [str(call) for call in mock_print.call_args_list]
                has_error = any("API_KEY" in call for call in printed_calls)
                assert has_error


class TestDisplayFunctions:
    """Test display and menu functions."""

    def test_display_header(self):
        """Test header display function."""
        with patch("builtins.print") as mock_print:
            display_header()

            # Check that header elements were printed
            printed_calls = [call.args[0] for call in mock_print.call_args_list]
            assert any("SAGE Research Agent" in call for call in printed_calls)
            assert any("Self-Adaptive" in call for call in printed_calls)

    def test_display_menu(self):
        """Test menu display function."""
        with patch("builtins.print") as mock_print:
            display_menu()

            # Check that menu options were printed
            printed_calls = [call.args[0] for call in mock_print.call_args_list]
            assert any("Quick Demo" in call for call in printed_calls)
            assert any("Basic Agent Test" in call for call in printed_calls)
            assert any("Enhanced Agent Test" in call for call in printed_calls)
            assert any("Exit" in call for call in printed_calls)

    def test_get_predefined_topics(self):
        """Test predefined topics retrieval."""
        topics = get_predefined_topics()

        assert isinstance(topics, dict)
        assert len(topics) > 0

        # Check structure of topics
        for _key, value in topics.items():
            assert "title" in value
            assert "topic" in value
            assert isinstance(value["title"], str)
            assert isinstance(value["topic"], str)
            assert len(value["title"]) > 0
            assert len(value["topic"]) > 0

    def test_predefined_topics_content(self):
        """Test that predefined topics contain expected content."""
        topics = get_predefined_topics()

        # Check for some expected topics
        titles = [topic["title"] for topic in topics.values()]
        topics_text = " ".join(titles)

        assert "Climate Tech" in topics_text or "Climate" in topics_text
        assert "AI" in topics_text or "Healthcare" in topics_text
        assert "Electric Vehicle" in topics_text or "EV" in topics_text


class TestAgentRunners:
    """Test agent runner functions."""

    def test_run_basic_agent_success(self, mock_api_keys):
        """Test successful basic agent run."""
        mock_agent = Mock()
        mock_agent.run.return_value = "Test research result"

        with patch("agent.SAGEAgent", return_value=mock_agent) as mock_sage_class:
            with patch("builtins.print"):
                result = run_basic_agent("Test research topic")

                assert result == "Test research result"
                mock_sage_class.assert_called_once()
                mock_agent.run.assert_called_once_with(goal="Test research topic")

    def test_run_basic_agent_no_result(self, mock_api_keys):
        """Test basic agent run with no result."""
        mock_agent = Mock()
        mock_agent.run.return_value = None

        with patch("agent.SAGEAgent", return_value=mock_agent):
            with patch("builtins.print") as mock_print:
                result = run_basic_agent("Test research topic")

                assert result is None
                # Check that some error message about no result was printed
                printed_calls = [call.args[0] for call in mock_print.call_args_list]
                error_found = any(
                    "did not produce a result" in call for call in printed_calls
                )
                assert error_found

    def test_run_basic_agent_import_error(self, mock_api_keys):
        """Test basic agent run with import error."""
        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            with patch("builtins.print") as mock_print:
                result = run_basic_agent("Test research topic")

                assert result is None
                mock_print.assert_any_call(
                    "❌ Basic agent (agent.py) not found or has import issues"
                )

    def test_run_basic_agent_general_exception(self, mock_api_keys):
        """Test basic agent run with general exception."""
        with patch("agent.SAGEAgent", side_effect=Exception("General error")):
            with patch("builtins.print") as mock_print:
                result = run_basic_agent("Test research topic")

                assert result is None
                mock_print.assert_any_call(
                    "❌ Error running basic agent: General error"
                )

    def test_run_enhanced_agent_success(self, mock_api_keys):
        """Test successful enhanced agent run."""
        mock_agent = Mock()
        mock_agent.run.return_value = "Enhanced research result"

        with patch(
            "enhanced_sage_agent.EnhancedSAGEAgent", return_value=mock_agent
        ) as mock_enhanced_class:
            with patch("builtins.print"):
                result = run_enhanced_agent("Test research topic")

                assert result == "Enhanced research result"
                mock_enhanced_class.assert_called_once()
                mock_agent.run.assert_called_once_with(
                    goal="Test research topic", max_iterations=20
                )

    def test_run_enhanced_agent_no_result(self, mock_api_keys):
        """Test enhanced agent run with no result."""
        mock_agent = Mock()
        mock_agent.run.return_value = None

        with patch("enhanced_sage_agent.EnhancedSAGEAgent", return_value=mock_agent):
            with patch("builtins.print") as mock_print:
                result = run_enhanced_agent("Test research topic")

                assert result is None
                # Check that some error message about no result was printed
                printed_calls = [call.args[0] for call in mock_print.call_args_list]
                error_found = any(
                    "did not produce a result" in call for call in printed_calls
                )
                assert error_found

    def test_run_enhanced_agent_import_error(self, mock_api_keys):
        """Test enhanced agent run with import error."""
        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            with patch("builtins.print") as mock_print:
                result = run_enhanced_agent("Test research topic")

                assert result is None
                expected_msg = "❌ Enhanced agent (enhanced_sage_agent.py) not found or has import issues"
                mock_print.assert_any_call(expected_msg)

    def test_run_enhanced_agent_general_exception(self, mock_api_keys):
        """Test enhanced agent run with general exception."""
        with patch(
            "enhanced_sage_agent.EnhancedSAGEAgent",
            side_effect=Exception("Enhanced error"),
        ):
            with patch("builtins.print") as mock_print:
                result = run_enhanced_agent("Test research topic")

                assert result is None
                mock_print.assert_any_call(
                    "❌ Error running enhanced agent: Enhanced error"
                )


class TestIntegration:
    """Integration tests for main script functionality."""

    def test_complete_workflow_simulation(self, mock_api_keys):
        """Test a complete workflow simulation."""
        # Mock both agents
        mock_basic_agent = Mock()
        mock_basic_agent.run.return_value = "Basic research complete"

        mock_enhanced_agent = Mock()
        mock_enhanced_agent.run.return_value = "Enhanced research complete"

        with (
            patch("agent.SAGEAgent", return_value=mock_basic_agent),
            patch(
                "enhanced_sage_agent.EnhancedSAGEAgent",
                return_value=mock_enhanced_agent,
            ),
            patch("builtins.print"),
        ):
            # Test basic agent
            basic_result = run_basic_agent("AI market analysis")
            assert basic_result == "Basic research complete"

            # Test enhanced agent
            enhanced_result = run_enhanced_agent("AI market analysis")
            assert enhanced_result == "Enhanced research complete"

            # Verify both were called with correct parameters
            mock_basic_agent.run.assert_called_with(goal="AI market analysis")
            mock_enhanced_agent.run.assert_called_with(
                goal="AI market analysis", max_iterations=20
            )

    def test_environment_and_agents_integration(self):
        """Test integration between environment checks and agent running."""
        # Test with missing environment
        with patch.dict(os.environ, {}, clear=True):
            assert check_environment() is False

        # Test with proper environment
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "test-key",
                "TAVILY_API_KEY": "test-key",
            },
        ):
            assert check_environment() is True

            # Now agents should be able to run (mocked)
            mock_agent = Mock()
            mock_agent.run.return_value = "Success"

            with (
                patch("agent.SAGEAgent", return_value=mock_agent),
                patch("builtins.print"),
            ):
                result = run_basic_agent("Test topic")
                assert result == "Success"
