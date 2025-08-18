# Agent Service Toolkit Transformation Guide

## Overview

This document provides instructions to transform the current agent-service-toolkit into a FastAPI-style framework through **in-place enhancement**. The transformation maintains 100% upstream compatibility while providing a simplified developer experience.

---

## 🤖 LLM Coding Assistant Instructions

### CRITICAL: This is an In-Place Enhancement

**This transforms the EXISTING agent-service-toolkit repository by ENHANCING existing files. Do NOT create new workspace, project, or separate package directories. Work within the current agent-service-toolkit directory by adding new functionality to existing files.**

### Startup Protocol

#### 1. Verify Existing Repository
- Confirm you are working in the agent-service-toolkit directory
- Verify existing files are present: `src/agents/`, `src/service/`, `pyproject.toml`, etc.
- DO NOT create new package directories - enhance existing files directly
- The transformation ADDS new functionality to existing `agents.py` and `service.py`

#### 2. Assess Current State
- Check if `IMPLEMENTATION_STATE.json` exists in project root
- If no state file: Create it with `echo '{"project_name": "agent-service-toolkit-transformation", "started_at": "'$(date -Iseconds)'", "current_phase": 1, "phases": {}}' > IMPLEMENTATION_STATE.json`
- If state file exists: Read current progress with `jq -r '.current_phase, .overall_progress, .next_actions[]?' IMPLEMENTATION_STATE.json`
- Review existing `src/agents/agents.py` and `src/service/service.py` to understand current implementation
- Identify the next incomplete step or phase

#### 3. Environment Verification
- Verify you are in the agent-service-toolkit project root
- Confirm tools available: `python --version`, `jq --version`, `git --version`
- Check existing project structure: `ls -la src/`
- Ensure no uncommitted changes that could cause conflicts

#### 4. Implementation Protocol
- Work through ONE complete phase at a time (6 phases total)
- ENHANCE existing files in `src/agents/agents.py` and `src/service/service.py` directly
- ADD new classes and functions alongside existing code patterns
- MAINTAIN 100% backward compatibility with existing agents and service
- Follow detailed instructions in `docs/transformation/IMPLEMENTATION_PHASES.md`
- STOP after completing each phase and request user confirmation
- Only proceed to next phase after explicit user approval
- Update `IMPLEMENTATION_STATE.json` after each completed step

### Mandatory Requirements

- ✅ Work within the EXISTING agent-service-toolkit repository
- ❌ NEVER create a new workspace, project, or separate package directory
- ✅ ENHANCE existing `src/agents/agents.py` and `src/service/service.py` files directly
- ✅ ADD new functionality alongside existing code (never replace existing code)
- ✅ NEVER mark anything complete without running verification commands
- ✅ NEVER proceed to next phase without user confirmation
- ✅ Always wait for user confirmation after each tool use
- ✅ Follow detailed implementation phases from linked documentation
- ✅ Use progress tracking from `docs/transformation/PROGRESS_TRACKING.md`
- ✅ Document blockers/issues in IMPLEMENTATION_STATE.json
- ✅ Ask for clarification if requirements are unclear
- ✅ Ensure existing functionality continues working throughout

---

## 🎯 Goals

1. **FastAPI-Style API**: Decorator-based agent registration similar to FastAPI routes
2. **PyPI Distribution**: Enhanced package that can be installed as dependency
3. **MCP Integration**: Automatic MCP server connection and tool discovery
4. **Zero Configuration**: Automatic persistence and lifecycle management
5. **Upstream Compatibility**: Non-breaking changes that can sync with original repo

## 📋 Current vs Target State

### Current State
```python
# Developers must clone entire repo and modify agents.py
from agents import agents
agent = agents["research-assistant"].graph
```

### Target State
```python
# Developers use enhanced agents.py with FastAPI-style decorator API
from agents import AgentService  # Enhanced agents.py exports AgentService

app = AgentService()

@app.agent("my-bot", description="My custom bot")
def create_bot():
    return compiled_graph

# OR use existing approach (100% backward compatible)
from agents import get_agent
agent = get_agent("research-assistant")

if __name__ == "__main__":
    app.run()
```

---

## 🏗️ Implementation Phases

| Phase | Description | Estimated Time | Key Files |
|-------|------------|---------------|-----------|
| **Phase 1** | Enhanced agents.py with AgentService Class | 2-3 days | `src/agents/agents.py` |
| **Phase 2** | Enhanced service.py with AgentService Support | 2-3 days | `src/service/service.py` |
| **Phase 3** | MCP Integration Support | 3-4 days | `src/agents/mcp_integration.py` |
| **Phase 4** | Package Configuration | 1-2 days | `pyproject.toml`, CLI |
| **Phase 5** | Testing and Verification | 2-3 days | `tests/` |
| **Phase 6** | Documentation and Examples | 2-3 days | `examples/`, `docs/` |

**Total Estimated Time: 12-18 days**

For detailed step-by-step instructions, see [Implementation Phases](docs/transformation/IMPLEMENTATION_PHASES.md).

---

## 📊 Progress Tracking

### Quick Status Check
```bash
# Check current state
test -f IMPLEMENTATION_STATE.json && echo "State file exists" || echo "Starting fresh"

# Verify environment
python --version && jq --version && git --version

# Check existing structure
ls -la src/ | head -10

# Read current progress (if state exists)
jq -r '.current_phase // 1, .phases | keys[]?' IMPLEMENTATION_STATE.json 2>/dev/null || echo "No phases started yet"
```

### State Management
For complete progress tracking instructions, see [Progress Tracking Guide](docs/transformation/PROGRESS_TRACKING.md).

---

## 🚀 Quick Start for LLM Assistants

**Use this single prompt to begin:**

```
Follow the LLM Coding Assistant Instructions in AGENT_SERVICE_TOOLKIT_TRANSFORMATION.md to implement the Agent Service Toolkit transformation. Start by reading the detailed implementation phases to understand the current state and next steps.
```

### Essential Reference Documents

- **[Implementation Phases](docs/transformation/IMPLEMENTATION_PHASES.md)**: Detailed step-by-step instructions
- **[Progress Tracking](docs/transformation/PROGRESS_TRACKING.md)**: State management and verification
- **[Migration Guide](docs/transformation/MIGRATION_GUIDE.md)**: Usage examples and API reference
- **[LLM Instructions](docs/transformation/LLM_ASSISTANT_INSTRUCTIONS.md)**: Detailed protocols for assistants

---

## ✅ Success Criteria

### Developer Experience
- [ ] Developers can `pip install agent-service-toolkit` (enhanced)
- [ ] Creating a new agent takes < 10 lines of code
- [ ] No knowledge of FastAPI internals required
- [ ] MCP tools work automatically
- [ ] Database persistence is transparent

### Technical Requirements
- [ ] Backward compatible with current repo
- [ ] All existing tests pass
- [ ] New framework has >95% test coverage
- [ ] Documentation is complete
- [ ] PyPI package builds successfully

### Integration Success
- [ ] Example apps run successfully
- [ ] Performance matches current implementation
- [ ] Memory usage is reasonable
- [ ] Error handling is robust
- [ ] Logging provides good debugging info

---

## 🔄 Emergency Rollback

If issues arise during implementation:

```bash
# Disable enhanced features (if implemented)
export AGENT_SERVICE_ENHANCED=false

# Revert to last known good state
git reset --hard <last_known_good_commit>

# Restore original functionality
git checkout HEAD~1 -- src/agents/agents.py src/service/service.py
```

---

## 📝 Implementation Notes

### Critical Success Factors

1. **Incremental Development**: Never implement all phases at once
2. **Backward Compatibility**: Existing `agents/agents.py` approach must continue working
3. **Testing Strategy**: Write tests for each component as you build it
4. **Documentation**: Update docs immediately after implementing features
5. **MCP Integration**: Start with simple, mock MCP servers before real integrations

### Expected Outcomes

After successful implementation:
- **Developers** can use enhanced framework immediately
- **Existing projects** continue to work without modification
- **New projects** benefit from simplified FastAPI-style API
- **MCP ecosystem** becomes easily accessible
- **Framework maintainers** can focus on core functionality

---

*This guide serves as the main entry point for the agent-service-toolkit transformation. Follow the phases sequentially, verify each step, and maintain backward compatibility throughout the process.*
