#!/usr/bin/env python3
"""
SAGE Research Agent - Interactive Demo
=====================================

This script provides an easy way to test and compare the basic and enhanced SAGE research agents.
Choose from predefined examples or input your own research topics.

Requirements:
- GOOGLE_API_KEY in environment or .env file
- TAVILY_API_KEY in environment or .env file
"""

import os
from datetime import datetime

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


def check_environment():
    """Check if required API keys are available."""
    google_key = os.getenv("GOOGLE_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    if not google_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please add it to your .env file or environment")
        return False

    if not tavily_key:
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("Please add it to your .env file or environment")
        return False

    print("✅ API keys found and ready")
    return True


def display_header():
    """Display the SAGE header and introduction."""
    print("\n" + "=" * 60)
    print("🎯 SAGE Research Agent - Interactive Demo")
    print("=" * 60)
    print("Self-Adaptive, Goal-Oriented AI Research Agent")
    print("Powered by Google Gemini & Tavily Search")
    print("-" * 60)


def display_menu():
    """Display the main menu options."""
    print("\n📋 Choose an option:")
    print("1. 🚀 Quick Demo - Enhanced Agent (Recommended)")
    print("2. 🔬 Basic Agent Test")
    print("3. ⚡ Enhanced Agent Test")
    print("4. 📊 Compare Both Agents")
    print("5. 🎯 Custom Research Topic")
    print("6. 📖 Example Research Topics")
    print("7. ❓ Help & Information")
    print("0. 🚪 Exit")
    print("-" * 60)


def get_predefined_topics():
    """Return a list of predefined research topics for testing."""
    return {
        "1": {
            "title": "🌍 Climate Tech Industry Analysis",
            "topic": "Write a comprehensive report on the climate technology industry, including market size, key players, emerging solutions, investment trends, and growth projections for 2025-2030.",
        },
        "2": {
            "title": "🤖 AI in Healthcare Market",
            "topic": "Analyze the artificial intelligence in healthcare market, covering current applications, major companies, regulatory challenges, and future opportunities.",
        },
        "3": {
            "title": "🚗 Electric Vehicle Market Trends",
            "topic": "Research the global electric vehicle market, including adoption rates, charging infrastructure, battery technology trends, and competitive landscape.",
        },
        "4": {
            "title": "💰 Fintech Innovation Report",
            "topic": "Examine the fintech industry landscape, focusing on digital payments, blockchain applications, regulatory developments, and emerging startups.",
        },
        "5": {
            "title": "🏠 Remote Work Technology Solutions",
            "topic": "Study the remote work technology market, including collaboration tools, security solutions, productivity software, and workplace trends.",
        },
        "6": {
            "title": "🔋 Renewable Energy Storage",
            "topic": "Investigate renewable energy storage technologies, market growth, key players, technological innovations, and future outlook.",
        },
    }


def run_basic_agent(topic):
    """Run the basic SAGE agent."""
    try:
        from agent import SAGEAgent

        print("\n🔬 Running Basic SAGE Agent...")
        print(f"📋 Topic: {topic}")
        print(f"⏰ Start time: {datetime.now()}")
        print("-" * 40)

        agent = SAGEAgent()
        result = agent.run(goal=topic)

        if result:
            print("\n✅ Basic agent completed successfully!")
            return result
        else:
            print("\n❌ Basic agent did not produce a result")
            return None

    except ImportError:
        print("❌ Basic agent (agent.py) not found or has import issues")
        return None
    except Exception as e:
        print(f"❌ Error running basic agent: {e}")
        return None


def run_enhanced_agent(topic):
    """Run the enhanced SAGE agent."""
    try:
        from enhanced_sage_agent import EnhancedSAGEAgent

        print("\n⚡ Running Enhanced SAGE Agent...")
        print(f"📋 Topic: {topic}")
        print(f"⏰ Start time: {datetime.now()}")
        print("-" * 40)

        agent = EnhancedSAGEAgent()
        result = agent.run(goal=topic, max_iterations=20)

        if result:
            print("\n✅ Enhanced agent completed successfully!")
            return result
        else:
            print("\n❌ Enhanced agent did not produce a result")
            return None

    except ImportError:
        print(
            "❌ Enhanced agent (enhanced_sage_agent.py) not found or has import issues"
        )
        return None
    except Exception as e:
        print(f"❌ Error running enhanced agent: {e}")
        return None


def quick_demo():
    """Run a quick demonstration with the enhanced agent."""
    print("\n🚀 Quick Demo - Enhanced SAGE Agent")
    print("This will run a short research example to demonstrate SAGE capabilities.\n")

    demo_topic = "Write a brief analysis of the current trends in sustainable technology, focusing on solar energy and electric vehicles."

    print(f"Demo topic: {demo_topic}\n")
    input("Press Enter to start the demo...")

    result = run_enhanced_agent(demo_topic)

    if result:
        print("\n🎉 Demo completed! Check the generated report file.")
        print(
            "The enhanced agent automatically saved the report with an intelligent filename."
        )

    return result


def compare_agents(topic):
    """Run both agents and compare their performance."""
    print("\n📊 Comparing Basic vs Enhanced SAGE Agents")
    print(f"📋 Topic: {topic}")
    print("=" * 60)

    # Run basic agent
    basic_start = datetime.now()
    basic_result = run_basic_agent(topic)
    basic_duration = datetime.now() - basic_start

    print("\n" + "=" * 60)

    # Run enhanced agent
    enhanced_start = datetime.now()
    enhanced_result = run_enhanced_agent(topic)
    enhanced_duration = datetime.now() - enhanced_start

    # Display comparison
    print("\n📊 Performance Comparison:")
    print("-" * 40)
    print("🔬 Basic Agent:")
    print(f"   ⏱️  Duration: {basic_duration}")
    print(f"   ✅ Success: {'Yes' if basic_result else 'No'}")

    print("\n⚡ Enhanced Agent:")
    print(f"   ⏱️  Duration: {enhanced_duration}")
    print(f"   ✅ Success: {'Yes' if enhanced_result else 'No'}")

    if basic_result and enhanced_result:
        print("\n📈 Results:")
        print(f"   📄 Basic report length: {len(basic_result)} characters")
        print(f"   📄 Enhanced report length: {len(enhanced_result)} characters")

    return basic_result, enhanced_result


def display_example_topics():
    """Display available example research topics."""
    topics = get_predefined_topics()

    print("\n📖 Example Research Topics:")
    print("=" * 50)

    for key, value in topics.items():
        print(f"\n{key}. {value['title']}")
        print(f"   📝 {value['topic'][:100]}...")

    print("\n7. 🎯 Custom Topic (Enter your own)")
    print("-" * 50)


def get_user_topic_choice():
    """Get user's choice of research topic."""
    topics = get_predefined_topics()

    while True:
        choice = input("\nSelect a topic (1-6) or 7 for custom: ").strip()

        if choice in topics:
            return topics[choice]["topic"]
        elif choice == "7":
            custom_topic = input("\nEnter your custom research topic: ").strip()
            if custom_topic:
                return custom_topic
            else:
                print("❌ Please enter a valid topic")
        else:
            print("❌ Please enter a number between 1-7")


def display_help():
    """Display help information."""
    print("\n❓ SAGE Research Agent Help")
    print("=" * 40)
    print("""
🎯 What is SAGE?
SAGE (Self-Adaptive, Goal-Oriented AI) is an intelligent research agent that:
- Conducts comprehensive research on any topic
- Uses multiple sources (web, news, academic, market research)
- Analyzes and synthesizes information intelligently
- Generates professional-quality reports

🔬 Basic vs Enhanced Agent:
• Basic Agent: Core functionality with simple web search and reasoning
• Enhanced Agent: Advanced features including:
  - Multi-source research (web, news, academic, market)
  - Quality assessment and iterative improvement
  - Smart caching for efficiency
  - Intelligent filename generation
  - Progress tracking and monitoring

⚡ Quick Start:
1. Ensure your API keys are set in .env file
2. Choose option 1 for a quick demo
3. Or select from predefined topics (option 6)
4. For custom research, choose option 5

🔧 Requirements:
- Google Generative AI API key (get from: https://makersuite.google.com/app/apikey)
- Tavily Search API key (get from: https://tavily.com/)

📁 Output:
- Reports are automatically saved as markdown files
- Filenames are intelligently generated with timestamps
- Files are saved in the current directory
""")


def main():
    """Main function to run the interactive SAGE demo."""
    display_header()

    # Check environment
    if not check_environment():
        print("\n🔧 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys to the .env file")
        print("3. Run this script again")
        return

    while True:
        display_menu()

        try:
            choice = input("\nEnter your choice (0-7): ").strip()

            if choice == "0":
                print("\n👋 Thank you for using SAGE Research Agent!")
                print("Visit: https://github.com/raythurman2386/research-agent")
                break

            elif choice == "1":
                quick_demo()

            elif choice == "2":
                topic = get_user_topic_choice()
                run_basic_agent(topic)

            elif choice == "3":
                topic = get_user_topic_choice()
                run_enhanced_agent(topic)

            elif choice == "4":
                topic = get_user_topic_choice()
                compare_agents(topic)

            elif choice == "5":
                custom_topic = input("\nEnter your research topic: ").strip()
                if custom_topic:
                    agent_choice = (
                        input("Use Enhanced agent? (y/n, default=y): ").strip().lower()
                    )
                    if agent_choice in ["n", "no"]:
                        run_basic_agent(custom_topic)
                    else:
                        run_enhanced_agent(custom_topic)
                else:
                    print("❌ Please enter a valid topic")

            elif choice == "6":
                display_example_topics()

            elif choice == "7":
                display_help()

            else:
                print("❌ Invalid choice. Please enter a number between 0-7.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or contact support.")

        # Pause before showing menu again
        if choice != "0":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
