#!/usr/bin/env python3
"""
MCP React Agent Example using AgentService

This demonstrates agent-level tool selection from MCP servers using the new
FastAPI-style decorator API with LangGraph's prebuilt React agent pattern.

NOTE: This example requires Phase 3 (MCP Integration) to be completed.
Currently demonstrates the intended API design.
"""

from langgraph.prebuilt import create_react_agent

from agents import AgentService
from core import get_model

# Initialize AgentService with MCP servers
app = AgentService(
    mcp_servers=[
        "npx -y @modelcontextprotocol/server-math",  # Provides calculator, geometry, etc.
        "npx -y @modelcontextprotocol/server-web",  # Provides web search tools
    ]
)


@app.agent("calculator-only-bot", description="Bot that only uses calculator from MCP math server")
def create_calculator_bot():
    """Agent that selects only calculator tool from MCP server."""
    model = get_model("gpt-3.5-turbo")

    # Agent-level tool selection: pick only calculator from MCP tools
    calculator_tool = app.get_mcp_tool("calculator")

    return create_react_agent(model=model, tools=[calculator_tool])


@app.agent("math-expert-bot", description="Bot that uses multiple math tools from MCP server")
def create_math_expert_bot():
    """Agent that selects multiple tools from the same MCP server."""
    model = get_model("gpt-4")

    # Select multiple tools from MCP math server
    calculator = app.get_mcp_tool("calculator")
    geometry = app.get_mcp_tool("geometry")

    return create_react_agent(model=model, tools=[calculator, geometry])


@app.agent("mixed-tools-bot", description="Bot mixing MCP and local tools")
def create_mixed_bot():
    """Agent that combines MCP tools with local tools."""
    from agents.tools import calculator as local_calc

    model = get_model("gpt-3.5-turbo")

    # Mix MCP tools with local tools
    mcp_search = app.get_mcp_tool("web_search")

    return create_react_agent(model=model, tools=[mcp_search, local_calc])


if __name__ == "__main__":
    print("🚀 Starting MCP React Agent Service...")
    print("📚 Agents use React (Reasoning + Acting) pattern")
    print("🔧 MCP Servers: math, web")
    print("🎯 Agent-level tool selection enabled")
    print("🌐 Access at: http://localhost:8000")
    print("📋 API docs at: http://localhost:8000/redoc")
    print()
    print("Available agents:")
    print("  • calculator-only-bot: Uses only calculator from MCP")
    print("  • math-expert-bot: Uses calculator + geometry from MCP")
    print("  • mixed-tools-bot: Combines MCP web search + local calculator")

    # Run the service (will connect to MCP servers on startup)
    app.run(host="0.0.0.0", port=8000, reload=True)
