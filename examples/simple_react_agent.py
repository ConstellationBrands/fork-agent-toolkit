#!/usr/bin/env python3
"""
Simple React Agent Example using AgentService

This demonstrates the new FastAPI-style decorator API with LangGraph's
prebuilt React agent pattern for the simplest possible agent creation.
"""

from langgraph.prebuilt import create_react_agent

from agents import AgentService
from agents.tools import calculator
from core import get_model

# Initialize the AgentService
app = AgentService()


@app.agent("math-helper", description="Simple math assistant using React pattern")
def create_math_agent():
    """Create a React agent that can do math calculations."""
    model = get_model("openai-compatible")

    # Use LangGraph's prebuilt create_react_agent for automatic ReAct pattern
    return create_react_agent(model=model, tools=[calculator])


if __name__ == "__main__":
    print("🚀 Starting Math Helper Agent Service...")
    print("📚 Agent uses React (Reasoning + Acting) pattern")
    print("🔧 Available tools: calculator")
    print("🌐 Access at: http://localhost:8000")
    print("📋 API docs at: http://localhost:8000/redoc")

    # Run the service
    app.run(host="0.0.0.0", port=8000, reload=True)
