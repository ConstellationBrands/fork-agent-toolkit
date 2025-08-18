# Migration Guide

## Overview

This guide helps developers migrate from the current agent-service-toolkit approach to the enhanced FastAPI-style framework. The enhanced framework provides 100% backward compatibility, so migration can be gradual and optional.

## Current vs Enhanced Approaches

### Current Approach (Continues to Work)

```python
# Existing method - no changes required
from agents import get_agent, agents

# Access existing agents
agent = get_agent("research-assistant")

# View all agents
all_agents = agents
```

### Enhanced Approach (New Capability)

```python
# New FastAPI-style framework
from agents import AgentService

app = AgentService()

@app.agent("my-bot", description="My custom bot")
def create_bot():
    return compiled_graph

if __name__ == "__main__":
    app.run()
```

## Migration Benefits

### Before Migration
- ✅ Works with existing infrastructure
- ❌ Requires modifying core agents.py file
- ❌ No clean separation of custom vs. framework code
- ❌ Manual persistence setup
- ❌ No automatic MCP integration
- ❌ Cannot distribute as standalone package

### After Migration  
- ✅ All existing functionality preserved
- ✅ Clean separation via decorators
- ✅ Automatic persistence and lifecycle management
- ✅ Built-in MCP server integration
- ✅ Can distribute as standalone package
- ✅ FastAPI-style developer experience

## Step-by-Step Migration

### Option 1: Keep Existing Approach
**No action required.** Your existing code will continue to work exactly as before.

### Option 2: Gradual Migration
Start using the enhanced approach for new agents while keeping existing ones:

```python
# Continue using existing agents
from agents import get_agent
research_agent = get_agent("research-assistant")

# Use enhanced approach for new agents
from agents import AgentService
app = AgentService()

@app.agent("my-new-agent")
def create_new_agent():
    return my_compiled_graph

if __name__ == "__main__":
    app.run()
```

### Option 3: Full Migration
Convert existing custom agent implementations to use the enhanced framework:

#### Before (Custom Agent in agents.py)
```python
# In src/agents/agents.py - modifying framework file
from agents.my_custom_agent import my_custom_agent

agents = {
    # ... existing agents
    "my-custom": Agent(
        description="My custom agent",
        graph=my_custom_agent
    ),
}
```

#### After (Standalone Application)
```python
# In your_project/main.py - clean separation
from agents import AgentService
from my_agents.my_custom_agent import create_my_custom_agent

app = AgentService(
    mcp_servers=[
        "npx -y @modelcontextprotocol/server-sequential-thinking"
    ]
)

@app.agent("my-custom", description="My custom agent")
def custom_agent_factory():
    return create_my_custom_agent()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## Migration Scenarios

### Scenario 1: Research Project
**Current:** Clone entire repo, modify agents.py, run full service

```bash
git clone https://github.com/JoshuaC215/agent-service-toolkit.git
cd agent-service-toolkit
# Modify src/agents/agents.py
python src/run_service.py
```

**Enhanced:** Create standalone project, use enhanced framework

```bash
pip install -e /path/to/enhanced-agent-service-toolkit
# Create main.py with AgentService
python main.py
```

### Scenario 2: Production Deployment
**Current:** Deploy entire repository with all example agents

**Enhanced:** Deploy only your specific agents with framework as dependency

```python
# requirements.txt
agent-service-toolkit>=0.1.0
# your specific dependencies only

# main.py - only your agents
from agents import AgentService
# ... your agent definitions only
```

### Scenario 3: Multi-Agent System
**Current:** All agents in single agents.py file

```python
# All in src/agents/agents.py
agents = {
    "agent1": Agent(...),
    "agent2": Agent(...), 
    "agent3": Agent(...),
}
```

**Enhanced:** Clean separation with enhanced features

```python
# main.py
app = AgentService(mcp_servers=["npx -y @mcp/thinking"])

@app.agent("agent1")
def create_agent1():
    return agent1_graph

@app.agent("agent2") 
def create_agent2():
    return agent2_graph

@app.agent("agent3")
def create_agent3():
    return agent3_graph
```

## API Reference

### AgentService Class

#### Constructor
```python
AgentService(
    checkpointer: str = "auto",      # Database for conversation memory
    store: str = "auto",             # Long-term memory store  
    mcp_servers: List[str] = None,   # MCP server configurations
    **kwargs
)
```

#### Methods

**`@app.agent(name, description="")`**
Register an agent with the service.

```python
@app.agent("my-agent", description="Description of what this agent does")
def create_agent():
    return compiled_langgraph_agent
```

**`create_app() -> FastAPI`**
Create the FastAPI application.

```python
fastapi_app = app.create_app()
# Use with ASGI servers like uvicorn, gunicorn
```

**`run(host=None, port=None, **kwargs)`**
Run development server.

```python
app.run(host="0.0.0.0", port=8000, reload=True)
```

### Generated Endpoints

Each registered agent automatically gets these endpoints:

- `POST /{agent_name}/invoke` - Synchronous invocation
- `POST /{agent_name}/stream` - Streaming invocation  
- `GET /info` - Service and agent information

### Request/Response Format

**Request:**
```json
{
  "message": "User message",
  "thread_id": "optional-conversation-id",
  "user_id": "optional-user-id",
  "model": "optional-model-override",
  "agent_config": {}
}
```

**Response:**
```json
{
  "type": "ai",
  "content": "Agent response",
  "run_id": "uuid-for-feedback",
  "metadata": {}
}
```

## Environment Configuration

### Required (at least one LLM provider)
```bash
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=...
# OR  
GOOGLE_API_KEY=...
```

### Optional Database Configuration
```bash
# Automatic detection if not specified
DATABASE_URL=postgresql://user:pass@host:port/db
MONGODB_URL=mongodb://host:port/db
```

### Optional MCP Server Configuration
```bash
# Can also be specified in AgentService constructor
MCP_SERVERS=server1,server2,server3
```

### Optional Service Configuration
```bash
HOST=0.0.0.0          # Default: 127.0.0.1
PORT=8000             # Default: 8000
AUTH_SECRET=secret    # Optional API key protection
```

## Advanced Usage

### Custom Persistence Configuration

```python
app = AgentService(
    checkpointer="postgresql://user:pass@host/db",
    store="mongodb://host:port/db"
)
```

### MCP Integration

```python
app = AgentService(mcp_servers=[
    "npx -y @modelcontextprotocol/server-sequential-thinking",
    "npx -y @modelcontextprotocol/server-filesystem", 
    "github.com/example/custom-mcp-server"
])
```

### Custom FastAPI Configuration

```python
app = AgentService()

# Register agents
@app.agent("my-agent")
def create_agent():
    return my_graph

# Get FastAPI instance for customization
fastapi_app = app.create_app()

# Add custom middleware, routes, etc.
fastapi_app.add_middleware(CustomMiddleware)

# Run with custom configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
```

## Troubleshooting

### Common Issues

**Import Error: `from agents import AgentService`**
- Solution: Ensure you're using the enhanced version of the toolkit
- Check: `ls src/agents/agents.py` should contain `AgentService` class

**Agent Not Found Error**
- Solution: Verify agent is registered with `@app.agent()` decorator
- Check: Agent name matches the endpoint URL

**MCP Tools Not Available**
- Solution: Check MCP server configuration and connectivity
- Debug: Look for MCP connection logs in application startup

**Database Connection Issues**
- Solution: Verify DATABASE_URL environment variable
- Fallback: Will use SQLite in memory if no database configured

### Migration Checklist

Before migrating:
- [ ] Backup existing implementation
- [ ] Test enhanced framework with simple agent
- [ ] Verify MCP servers are accessible
- [ ] Confirm database connectivity
- [ ] Test all endpoints with existing clients

During migration:
- [ ] Preserve existing agent functionality
- [ ] Test backward compatibility
- [ ] Verify performance characteristics
- [ ] Confirm error handling behavior
- [ ] Test with production data

After migration:
- [ ] Monitor application performance
- [ ] Verify logging and metrics
- [ ] Test failure recovery
- [ ] Validate security configuration
- [ ] Update deployment documentation

## Support and Resources

### Documentation
- [Implementation Phases](IMPLEMENTATION_PHASES.md) - Step-by-step transformation guide
- [Progress Tracking](PROGRESS_TRACKING.md) - State management and verification
- [LLM Assistant Instructions](LLM_ASSISTANT_INSTRUCTIONS.md) - For automated implementation

### Example Applications
- `examples/enhanced_framework/main.py` - Basic usage example
- `examples/fastapi_style/` - FastAPI-style patterns
- `examples/mcp_integration/` - MCP server integration examples

### Getting Help
- Check existing agent implementations for patterns
- Review test files for usage examples
- Consult FastAPI documentation for advanced customization
- Review LangGraph documentation for agent development

---

*This migration guide provides comprehensive information for transitioning to the enhanced Agent Service Toolkit framework while maintaining full backward compatibility.*
