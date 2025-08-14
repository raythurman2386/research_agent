import json
import os
import re
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from tavily import TavilyClient


# --- 1. Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@dataclass
class ResearchContext:
    """Maintains research context and state."""

    goal: str
    start_time: datetime
    sources: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    current_phase: str
    confidence_score: float
    iteration_count: int
    research_outline: dict[str, Any] | None = None


class ResearchDatabase:
    """Persistent storage for research data."""

    def __init__(self, db_path: str = "research_cache.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for caching research."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_cache (
                query TEXT PRIMARY KEY,
                results TEXT,
                timestamp DATETIME,
                source TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_sessions (
                session_id TEXT PRIMARY KEY,
                goal TEXT,
                start_time DATETIME,
                end_time DATETIME,
                status TEXT,
                final_report TEXT
            )
        """)
        conn.commit()
        conn.close()

    def cache_search_result(self, query: str, results: str, source: str):
        """Cache search results to avoid duplicate queries."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO search_cache
            (query, results, timestamp, source) VALUES (?, ?, ?, ?)
        """,
            (query, results, datetime.now(), source),
        )
        conn.commit()
        conn.close()

    def get_cached_result(self, query: str, max_age_hours: int = 24) -> str | None:
        """Retrieve cached search results if recent enough."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT results FROM search_cache
            WHERE query = ? AND
            datetime(timestamp) > datetime('now', '-{max_age_hours} hours')
        """,
            (query,),
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None


# --- 2. Enhanced Tool Definitions ---


def web_search(query: str) -> str:
    """Performs a comprehensive web search to find information on a topic.

    Args:
        query: The search query string

    Returns:
        JSON string containing search results
    """
    print(f"TOOL: Searching for '{query}'...")

    # Check cache first
    db = ResearchDatabase()
    cached_result = db.get_cached_result(query)
    if cached_result:
        print("TOOL: Using cached search result")
        return cached_result

    try:
        response = tavily_client.search(query=query, search_depth="advanced")
        result = json.dumps(response.get("results", []))
        db.cache_search_result(query, result, "tavily")
        return result
    except Exception as e:
        return f"Error during search: {e}"


def news_search(query: str) -> str:
    """Searches for recent news articles on a specific topic.

    Args:
        query: The news search query

    Returns:
        JSON string containing news search results
    """
    print(f"TOOL: Searching news for '{query}'...")

    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            include_domains=[
                "reuters.com",
                "bloomberg.com",
                "techcrunch.com",
                "cnbc.com",
            ],
        )
        return json.dumps(response.get("results", []))
    except Exception as e:
        return f"Error during news search: {e}"


def academic_search(query: str) -> str:
    """Searches for academic and research papers on a topic.

    Args:
        query: The academic search query

    Returns:
        JSON string containing academic search results
    """
    print(f"TOOL: Searching academic sources for '{query}'...")

    try:
        academic_query = (
            query
            + " site:scholar.google.com OR site:arxiv.org OR site:researchgate.net"
        )
        response = tavily_client.search(query=academic_query, search_depth="advanced")
        return json.dumps(response.get("results", []))
    except Exception as e:
        return f"Error during academic search: {e}"


def market_research(query: str) -> str:
    """Searches for market research reports and industry analysis.

    Args:
        query: The market research query

    Returns:
        JSON string containing market research results
    """
    print(f"TOOL: Searching market research for '{query}'...")

    try:
        market_query = query + " market research report analysis industry trends"
        response = tavily_client.search(query=market_query, search_depth="advanced")
        return json.dumps(response.get("results", []))
    except Exception as e:
        return f"Error during market research: {e}"


def analyze_data(data_description: str) -> str:
    """Performs analysis on gathered research data.

    Args:
        data_description: Description of the data to analyze

    Returns:
        Analysis results and insights
    """
    print(f"TOOL: Analyzing data - '{data_description[:50]}...'")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze the following research data and provide insights:
    {data_description}

    Focus on:
    1. Key trends and patterns
    2. Market dynamics
    3. Competitive landscape
    4. Growth opportunities
    5. Potential challenges

    Provide a structured analysis with specific data points where available.
    """

    response = model.generate_content(prompt)
    return response.text


def create_outline(topic: str) -> str:
    """Generates a comprehensive research outline for a given topic.

    Args:
        topic: The research topic

    Returns:
        Structured research outline
    """
    print(f"TOOL: Creating research outline for '{topic}'")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Create a comprehensive research outline for: {topic}

    Include:
    1. Executive Summary structure
    2. Key research questions
    3. Primary research areas
    4. Data sources to investigate
    5. Analysis methodologies
    6. Expected deliverables

    Format as a clear, structured outline.
    """

    response = model.generate_content(prompt)
    return response.text


def quality_check(content: str) -> str:
    """Evaluates the quality and completeness of research content.

    Args:
        content: Research content to evaluate

    Returns:
        Quality assessment and recommendations
    """
    print("TOOL: Performing quality assessment")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Evaluate the quality and completeness of this research content:

    {content}

    Assess:
    1. Completeness (1-10 score)
    2. Accuracy and reliability (1-10 score)
    3. Depth of analysis (1-10 score)
    4. Source diversity (1-10 score)
    5. Areas needing improvement
    6. Missing critical information
    7. Overall quality score (1-10)

    Provide specific recommendations for improvement.
    """

    response = model.generate_content(prompt)
    return response.text


def generate_filename(research_topic: str) -> str:
    """Generates an intelligent, descriptive filename for the research report.

    Args:
        research_topic: The main topic or goal of the research

    Returns:
        A well-formatted filename with timestamp
    """
    print("TOOL: Generating intelligent filename...")

    try:
        # Create a descriptive filename based on the research topic
        # Extract key terms from the topic
        topic_lower = research_topic.lower()

        if "geospatial" in topic_lower and "software" in topic_lower:
            base_name = "Geospatial-Software-Industry-Analysis"
        elif "market" in topic_lower and "analysis" in topic_lower:
            base_name = "Market-Analysis-Report"
        elif "industry" in topic_lower and "report" in topic_lower:
            base_name = "Industry-Research-Report"
        elif "competitive" in topic_lower and "landscape" in topic_lower:
            base_name = "Competitive-Landscape-Study"
        else:
            # Fallback: create from first few meaningful words
            words = re.findall(r"\b\w+\b", research_topic)
            meaningful_words = [
                w
                for w in words[:5]
                if len(w) > 2 and w.lower() not in ["the", "and", "for", "with"]
            ]
            base_name = "-".join(word.title() for word in meaningful_words[:4])

        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{base_name}_{timestamp}.md"

        return full_filename
    except Exception:
        # Fallback to simple naming if generation fails
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"Research-Report_{timestamp}.md"


def finish_research(final_report_markdown: str) -> str:
    """Finalizes the research and saves the comprehensive report.

    Args:
        final_report_markdown: The complete research report in markdown format

    Returns:
        Confirmation message
    """
    print("TOOL: Finalizing research report")

    # Save to database
    db = ResearchDatabase()
    session_id = f"session_{int(time.time())}"

    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO research_sessions
        (session_id, goal, start_time, end_time, status, final_report)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            session_id,
            "Research Goal",
            datetime.now(),
            datetime.now(),
            "completed",
            final_report_markdown,
        ),
    )
    conn.commit()
    conn.close()

    return final_report_markdown


# --- 3. Enhanced SAGE Agent Class ---


class EnhancedSAGEAgent:
    """An Enhanced Self-Adaptive, Goal-Oriented AI Agent with advanced capabilities."""

    def __init__(self, model_name="gemini-1.5-pro-latest"):
        self.tools = {
            "web_search": web_search,
            "news_search": news_search,
            "academic_search": academic_search,
            "market_research": market_research,
            "analyze_data": analyze_data,
            "create_outline": create_outline,
            "quality_check": quality_check,
            "finish_research": finish_research,
        }

        self.context = None
        self.db = ResearchDatabase()

        self.system_prompt = """You are an Enhanced SAGE Agent, a Self-Adaptive, Goal-Oriented AI Researcher.

Your capabilities include:
- Comprehensive web search across multiple source types
- Academic and market research
- Data analysis and quality assessment
- Research planning and execution

Process:
1. Create a research outline to plan your approach
2. Gather information using different search types (web, news, academic, market)
3. Analyze gathered data for insights and patterns
4. Assess quality and identify gaps
5. Continue research to fill gaps if needed
6. Finalize comprehensive report when complete

Available tools:
- web_search: General web search
- news_search: Recent news and current events
- academic_search: Academic papers and research
- market_research: Industry reports and market analysis
- analyze_data: Analyze gathered information
- create_outline: Generate research structure
- quality_check: Assess research completeness
- finish_research: Complete the research with final report

Your response MUST be a function call. Work systematically and thoroughly."""

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self.system_prompt,
            tools=list(self.tools.values()),
            safety_settings=self.safety_settings,
        )

    def run(self, goal: str, max_iterations: int = 20):
        """Enhanced run method with iteration limits and progress tracking."""
        print("🎯 Starting Enhanced SAGE Agent")
        print(f"📋 Goal: {goal}")
        print(f"⏰ Start time: {datetime.now()}")
        print(f"🔄 Max iterations: {max_iterations}\n")

        # Initialize research context
        self.context = ResearchContext(
            goal=goal,
            start_time=datetime.now(),
            sources=[],
            findings=[],
            current_phase="planning",
            confidence_score=0.0,
            iteration_count=0,
        )

        chat = self.model.start_chat()

        try:
            response = chat.send_message(goal)
        except Exception as e:
            print(f"Error starting chat: {e}")
            return None

        final_report = None

        while self.context.iteration_count < max_iterations:
            self.context.iteration_count += 1
            print(f"\n--- Iteration {self.context.iteration_count} ---")

            try:
                latest_part = response.candidates[0].content.parts[0]

                if (
                    not hasattr(latest_part, "function_call")
                    or not latest_part.function_call
                ):
                    print("AGENT: Model did not call a tool. Ending loop.")
                    break

                function_call = latest_part.function_call
                tool_name = function_call.name
                tool_args = dict(function_call.args)

                print(f"🔧 Tool: {tool_name}")
                print(f"📝 Args: {tool_args}")

                if tool_name == "finish_research":
                    print("AGENT: Research completed. Finalizing report.")
                    final_report = tool_args.get("final_report_markdown")
                    break

                if tool_name in self.tools:
                    tool_function = self.tools[tool_name]
                    try:
                        tool_result = tool_function(**tool_args)

                        # Track research progress
                        if tool_name in [
                            "web_search",
                            "news_search",
                            "academic_search",
                            "market_research",
                        ]:
                            self.context.sources.append(
                                {
                                    "type": tool_name,
                                    "query": tool_args.get("query", ""),
                                    "timestamp": datetime.now(),
                                }
                            )

                        function_response = genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name, response={"result": tool_result}
                            )
                        )
                        response = chat.send_message([function_response])

                    except Exception as e:
                        print(f"AGENT: Error executing tool {tool_name}: {e}")
                        function_response = genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name, response={"error": str(e)}
                            )
                        )
                        response = chat.send_message([function_response])
                else:
                    print(f"AGENT: Unknown tool '{tool_name}' called by model.")
                    break

            except Exception as e:
                print(f"AGENT: Error in iteration {self.context.iteration_count}: {e}")
                break

        # Generate research summary
        if final_report:
            self._generate_research_summary()

        return final_report

    def _generate_research_summary(self):
        """Generate a summary of the research process."""
        print("\n📊 Research Summary:")
        print(f"⏱️  Duration: {datetime.now() - self.context.start_time}")
        print(f"🔄 Iterations: {self.context.iteration_count}")
        print(f"📚 Sources consulted: {len(self.context.sources)}")
        print(f"🎯 Current phase: {self.context.current_phase}")


# --- 4. Main Execution ---

if __name__ == "__main__":
    agent = EnhancedSAGEAgent()

    research_goal = """Write a comprehensive report on the current state of the Geospatial Software Development Industry, including market size analysis, competitive landscape, emerging technologies, key industry trends, investment patterns, and future outlook for 2025-2030."""

    final_report = agent.run(goal=research_goal, max_iterations=25)

    if final_report:
        # Generate intelligent filename based on the research goal
        filename = generate_filename(research_goal)

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_report)
            print(f"\n🎉 Successfully saved the enhanced report as '{filename}'")
        except OSError as e:
            print(f"\n🚨 Error saving file: {e}")
    else:
        print("\n❌ Agent did not produce a final report.")
