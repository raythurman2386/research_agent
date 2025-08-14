import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from tavily import TavilyClient


# --- 1. Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# --- 2. Tool Definitions ---
# These are the Python functions the agent can execute.


def web_search(query: str) -> str:
    """Performs a web search to find information on a topic."""
    print(f"TOOL: Searching for '{query}'...")
    try:
        response = tavily_client.search(query=query, search_depth="advanced")
        return json.dumps(response.get("results", []))
    except Exception as e:
        return f"Error during search: {e}"


def reasoning_tool(sub_task_prompt: str) -> str:
    """Uses a model for reasoning, analysis, or summarization of existing data."""
    print(f"TOOL: Reasoning about '{sub_task_prompt[:50]}...'")
    # This is a simplified tool. In a real scenario, you might pass
    # the existing conversation history to another model instance.
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(sub_task_prompt)
    return response.text


def finish_research(final_report_markdown: str) -> str:
    """Concludes the research and provides the final, comprehensive report."""
    print("TOOL: Finishing research.")
    return final_report_markdown


# --- 3. SAGE Agent Class ---


class SAGEAgent:
    """A Self-Adaptive, Goal-Oriented AI Agent."""

    def __init__(self, model_name="gemini-1.5-pro-latest"):
        self.tools = {
            "web_search": web_search,
            "reasoning_tool": reasoning_tool,
            "finish_research": finish_research,
        }
        self.system_prompt = """
        You are a SAGE Agent, a Self-Adaptive, Goal-Oriented AI Researcher.
        Your purpose is to achieve a user's goal by iteratively assessing your progress,
        planning next steps, and executing tasks using the available tools.

        Follow this process:
        1. **Assess:** Review the goal and conversation history. Determine your progress and what is missing.
        2. **Plan:** Decide on the single most important next step to take.
        3. **Execute:** Call the single tool that best accomplishes your planned step.

        Your response MUST be a function call. Do not reply with text.
        Continue this cycle until you have enough information to create a comprehensive report
        and can call `finish_research`. Work autonomously.
        """
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=self.system_prompt,
            tools=self.tools.values(),
            safety_settings=self.safety_settings,
        )

    def run(self, goal: str):
        """Runs the agent to achieve a goal."""
        # Use the high-level chat session, which automatically manages history.
        chat = self.model.start_chat()

        # Kick off the process with the initial goal.
        response = chat.send_message(goal)
        final_report = None

        # Start the agent loop
        while True:
            latest_part = response.candidates[0].content.parts[0]

            if not latest_part.function_call:
                print("AGENT: Model did not call a tool. Ending loop.")
                break

            # Extract the tool call details
            function_call = latest_part.function_call
            tool_name = function_call.name
            tool_args = dict(function_call.args)

            # Check for the exit condition
            if tool_name == "finish_research":
                print("AGENT: Goal achieved. Finalizing report.")
                final_report = tool_args.get("final_report_markdown")
                break  # Exit the loop

            # Execute the chosen tool
            if tool_name in self.tools:
                tool_function = self.tools[tool_name]
                try:
                    tool_result = tool_function(**tool_args)
                    # Send the tool's result back to the model.
                    # Create the function response and send it
                    function_response = genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name, response={"result": tool_result}
                        )
                    )
                    response = chat.send_message(function_response)
                except Exception as e:
                    print(f"AGENT: Error executing tool {tool_name}: {e}")
                    # Send an error message back to the model
                    function_response = genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name, response={"error": str(e)}
                        )
                    )
                    response = chat.send_message(function_response)
            else:
                print(f"AGENT: Unknown tool '{tool_name}' called by model.")
                break

        return final_report


def _create_filename_from_goal(goal: str) -> str:
    """Creates a safe filename from the goal string."""
    sanitized = re.sub(r"[^\w\s-]", "", goal).strip().lower()
    sanitized = re.sub(r"[-\s]+", "-", sanitized)
    return f"SAGE_Report_{sanitized[:50]}.md"


# --- 4. Main Execution ---

if __name__ == "__main__":
    agent = SAGEAgent()

    research_goal = "Write a comprehensive report on the current state of the Geospatial Software Development Industry, focusing on key players, emerging trends, and market size."

    print(f"🎯 Starting SAGE Agent with Goal: {research_goal}\n")

    final_report = agent.run(goal=research_goal)

    if final_report:
        filename = _create_filename_from_goal(research_goal)
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_report)
            print(f"\n🎉 Successfully saved the report as '{filename}'")
        except OSError as e:
            print(f"\n🚨 Error saving file: {e}")
    else:
        print("\n Agent did not produce a final report.")
