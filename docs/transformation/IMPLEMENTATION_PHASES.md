# Implementation Phases - Agent Service Toolkit Transformation

This document provides directional instructions for implementing all 6 transformation phases. Each phase focuses on **what** to build and **where** to integrate, allowing LLMs to generate optimal implementations.

---

## Phase 1: Enhanced agents.py with AgentService Class

**Objective**: Add the `AgentService` class directly to `src/agents/agents.py`

### 1.1 Add AgentService Class to agents.py

**File**: `src/agents/agents.py` (ENHANCE existing file)

**Requirements:**
- ADD `AgentService` class at the END of existing file (after all existing code)
- IMPLEMENT FastAPI-style decorator pattern with `@app.agent(name, description)`
- SUPPORT agent registration via decorator that stores `AgentFactory` callables
- INCLUDE initialization parameters: `checkpointer`, `store`, `mcp_servers`
- MAINTAIN internal registries: `_agents: Dict[str, AgentFactory]` and `_agent_descriptions`
- CREATE `create_app()` method that calls `service.service.create_enhanced_app(self)`
- CREATE `run()` method that uses uvicorn with settings from `core.settings`
- IMPORT required types: `AsyncGenerator`, `Callable`, `Dict`, `List`, `Optional`
- USE type alias: `AgentFactory = Callable[[], AgentGraph]`

**Integration Points:**
- APPEND to existing file, do not modify existing code
- MAINTAIN compatibility with existing `agents` dictionary
- ENSURE existing imports continue working

### 1.2 Add Enhanced Helper Functions

**File**: `src/agents/agents.py` (ADD new functions)

**Requirements:**
- ADD `get_agent_enhanced()` function that checks AgentService first, then falls back to legacy
- ADD `get_all_agent_info_enhanced()` function that combines legacy and AgentService agents
- UPDATE `__all__` exports to include new functionality
- MAINTAIN 100% backward compatibility with existing functions

**Verification Commands**:
```bash
# Test enhanced agents.py import
cd src && python -c "from agents import AgentService; print('✅ AgentService import successful')"

# Test backward compatibility
cd src && python -c "from agents import get_agent, agents; print('✅ Legacy imports still work')"

# Test basic AgentService instantiation
cd src && python -c "from agents import AgentService; app = AgentService(); print('✅ AgentService created')"

# Verify existing agent registry still works
cd src && python -c "
from agents import get_agent, agents
agent = get_agent('research-assistant')
print(f'✅ Legacy agent access works: {type(agent).__name__}')
"

# Verify existing imports unchanged
cd src && python -c "
from agents import DEFAULT_AGENT, AgentGraph, Agent
print('✅ All existing exports available')
"

# Run existing tests to ensure no regression
pytest tests/ -k "test_" --tb=short
```

---

## Phase 2: Enhanced service.py with AgentService Support

**Objective**: Modify `src/service/service.py` to support both legacy agents and AgentService instances

### 2.1 Add Enhanced App Creation Function

**File**: `src/service/service.py` (ADD new function)

**Requirements:**
- ADD `create_enhanced_app(agent_service_instance=None)` function BEFORE existing app creation
- IMPLEMENT enhanced lifespan manager using `@asynccontextmanager`
- REUSE existing database/store initialization (unchanged behavior)
- CONFIGURE legacy agents exactly as current implementation
- ADD AgentService agent configuration when `agent_service_instance` provided:
  - Store AgentService instance in `app.state.agent_service`
  - Initialize MCP connections if `_mcp_servers` configured
  - Configure each AgentService agent with checkpointer and store
  - Bind MCP tools to agents if available
  - Store configured agents in `app.state.configured_agents`
- CREATE FastAPI app with enhanced lifespan and include existing router
- HANDLE errors gracefully with logging

### 2.2 Add Enhanced Agent Resolution Function

**File**: `src/service/service.py` (ADD new function)

**Requirements:**
- ADD `get_agent_with_service(agent_id: str, request=None) -> AgentGraph` after `_handle_input`
- CHECK `request.app.state.configured_agents` first for AgentService agents
- FALLBACK to `request.app.state.agent_service._agents` if configured_agents not found
- FALLBACK to existing `get_agent(agent_id)` for full backward compatibility
- MAINTAIN 100% compatibility with legacy system

### 2.3 Update Route Handlers for Enhanced Agent Resolution

**File**: `src/service/service.py` (MODIFY existing functions)

**Requirements:**
- UPDATE `invoke` function signature to accept `request: Request = None`
- REPLACE `get_agent(agent_id)` calls with `get_agent_with_service(agent_id, request)`
- UPDATE `message_generator` function signature to accept `request: Request = None`
- UPDATE stream endpoint to pass request parameter
- IMPORT `Request` from `fastapi`
- MAINTAIN all existing functionality and error handling

**Verification Commands**:
```bash
# Test enhanced service import
cd src && python -c "from service.service import create_enhanced_app; print('✅ Enhanced service functions available')"

# Test service creation with AgentService
cd src && python -c "
from agents import AgentService
from service.service import create_enhanced_app
app_service = AgentService()
fastapi_app = create_enhanced_app(app_service)
print('✅ Enhanced FastAPI app created')
"

# Verify existing service still works
cd src && python -c "
from service.service import app
print('✅ Legacy service app still available')
"
```

---

## Phase 3: MCP Integration Support

**Objective**: Add MCP server integration capabilities to the enhanced framework

### 3.1 Create MCP Integration Module

**File**: `src/agents/mcp_integration.py` (NEW file)

**Requirements:**
- CREATE `MCPIntegration` class that manages server connections and tool discovery
- IMPLEMENT `connect_and_discover_tools()` method that returns list of LangChain `Tool` objects
- SUPPORT multiple server types: NPX packages, GitHub repos, custom servers
- IMPLEMENT MCP protocol communication using JSON-RPC 2.0 format
- HANDLE server startup via `asyncio.create_subprocess_exec` for NPX servers
- IMPLEMENT MCP handshake: send "initialize" message with protocol version "2024-11-05"
- DISCOVER tools via "tools/list" method call
- CONVERT MCP tool definitions to LangChain Tool objects with async functions
- IMPLEMENT tool execution via "tools/call" method with proper argument passing
- HANDLE connection errors gracefully with logging
- PROVIDE `disconnect_all()` method for cleanup

**Protocol Implementation:**
- USE JSON-RPC 2.0 format for all MCP communications
- SEND initialize message with client info {"name": "agent-service-toolkit", "version": "0.1.0"}
- PARSE tool schemas and convert to LangChain tool format
- HANDLE timeouts and error responses appropriately
- LOG connection status and tool discovery results

**Integration Points:**
- IMPORT `Tool` from `langchain_core.tools`
- USE `asyncio` for subprocess management
- IMPLEMENT proper logging with module logger
- SUPPORT different server configuration formats

**Verification Commands**:
```bash
# Test MCP integration import
cd src && python -c "from agents.mcp_integration import MCPIntegration; print('✅ MCP Integration import successful')"

# Test basic MCP setup (without actual servers)
cd src && python -c "
from agents.mcp_integration import MCPIntegration
mcp = MCPIntegration([])
print('✅ MCP Integration created')
"
```

---

## Phase 4: Package Configuration

**Objective**: Configure pyproject.toml and CLI for enhanced framework

### 4.1 Update pyproject.toml for Enhanced Framework

**File**: `pyproject.toml` (MODIFY existing file)

**Requirements:**
- ADD CLI entry point: `agent-service-toolkit = "agents.cli:main"` to `[project.scripts]`
- ADD new dependency group `framework` with minimal dependencies:
  - fastapi, langchain-core, langgraph, pydantic, uvicorn
- ADD `enhanced` dependency group that references framework group
- MAINTAIN existing dependency groups and project configuration

### 4.2 Create CLI Interface for Enhanced Framework

**File**: `src/agents/cli.py` (NEW file)

**Requirements:**
- CREATE command-line interface with `argparse`
- IMPLEMENT `load_agent_service_from_file()` function using `importlib.util`
- SUPPORT app loading with format "file.py:app" (defaults to "app" if no colon)
- VALIDATE loaded object is AgentService instance
- IMPLEMENT `run` command that calls `agent_service.run()`
- SUPPORT CLI arguments: `--host`, `--port`, `--reload`
- HANDLE import and module loading errors gracefully
- PROVIDE help text for all commands and arguments

**Integration Points:**
- IMPORT AgentService for type validation
- USE uvicorn for development server (via AgentService.run())
- HANDLE file path resolution and module loading

**Verification Commands**:
```bash
# Test CLI import
cd src && python -c "from agents.cli import main; print('✅ CLI import successful')"

# Test package build (dry run)
python -m build --wheel --outdir dist/

# Test CLI help
cd src && python -m agents.cli --help
```

---

## Phase 5: Testing and Verification

**Objective**: Create comprehensive tests for the enhanced framework

### 5.1 Core Framework Tests

**File**: `tests/agents/test_agent_service.py` (NEW file)

**Requirements:**
- CREATE comprehensive test suite for AgentService functionality
- TEST basic AgentService creation and initialization
- TEST agent decorator registration and storage
- TEST backward compatibility with existing imports
- TEST enhanced get_agent function behavior
- TEST FastAPI app creation via create_app()
- USE pytest fixtures for sample LangGraph agents
- MOCK external dependencies appropriately
- VERIFY agent registry management
- TEST error handling and edge cases

### 5.2 Service Integration Tests

**File**: `tests/service/test_enhanced_service.py` (NEW file)

**Requirements:**
- CREATE tests for enhanced service integration
- TEST enhanced lifespan management with mocked dependencies
- TEST agent resolution with request context
- TEST fallback behavior to legacy system
- MOCK database and store initialization
- TEST MCP integration during lifespan
- VERIFY AgentService agents configuration
- TEST error handling in service layer
- ENSURE backward compatibility maintained

**Verification Commands**:
```bash
# Run existing tests to ensure no regression
pytest tests/ -v --tb=short

# Run new tests
pytest tests/agents/test_agent_service.py -v
pytest tests/service/test_enhanced_service.py -v

# Test that all existing functionality still works
cd src && python -c "
from agents import get_agent, agents
from service.service import app
print('✅ All legacy functionality preserved')
"

# Test new functionality
cd src && python -c "
from agents import AgentService
app = AgentService()
print('✅ New AgentService functionality available')
"
```

---

## Phase 6: Documentation and Examples

**Objective**: Create usage examples and documentation for the enhanced framework

### 6.1 Enhanced Usage Example

**File**: `examples/enhanced_framework/main.py` (NEW file)

**Requirements:**
- CREATE example showing FastAPI-style decorator usage
- DEMONSTRATE AgentService instantiation with MCP server configuration
- IMPLEMENT simple chatbot using StateGraph and decorator registration
- SHOW proper state management with LangChain message types
- INCLUDE server startup with development configuration
- USE realistic chat node implementation with state handling
- DEMONSTRATE MCP server integration example

**Key Patterns to Show:**
- AgentService instantiation: `app = AgentService(mcp_servers=[...])`
- Agent registration: `@app.agent("name", description="...")`
- StateGraph usage with proper state class
- Development server startup: `app.run(host="0.0.0.0", port=8000, reload=True)`

### 6.2 Mixed Usage Example

**File**: `examples/mixed_approach/main.py` (NEW file)

**Requirements:**
- DEMONSTRATE compatibility between legacy and enhanced approaches
- SHOW legacy agent access: `get_agent("research-assistant")`
- SHOW enhanced agent creation using AgentService
- DEMONSTRATE both approaches working together
- INCLUDE informational output showing both systems
- PROVIDE example of gradual migration approach

**Integration Patterns:**
- Legacy agent usage alongside AgentService
- Mixed import strategy from agents module
- Demonstrating backward compatibility
- Showing migration path for existing projects

**Verification Commands**:
```bash
# Test examples
cd examples/enhanced_framework && python main.py &
sleep 2 && curl http://localhost:8000/info && kill %1

# Test mixed approach
cd examples/mixed_approach && python main.py &
sleep 2 && curl http://localhost:8000/info && kill %1

# Test CLI with example
cd examples/enhanced_framework && python -m agents.cli run main.py:app --help
```

---

## Summary

This completes all 6 phases of the Agent Service Toolkit transformation:

1. **Phase 1**: Enhanced `agents.py` with `AgentService` class
2. **Phase 2**: Enhanced `service.py` with AgentService support
3. **Phase 3**: MCP integration capabilities
4. **Phase 4**: Package configuration and CLI
5. **Phase 5**: Comprehensive testing framework
6. **Phase 6**: Documentation and usage examples

The transformation maintains 100% backward compatibility while providing a modern, FastAPI-style API for new development.
