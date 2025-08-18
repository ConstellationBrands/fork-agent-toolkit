# LLM Assistant Implementation Instructions

## Overview

This document provides detailed protocols for LLM coding assistants to implement the Agent Service Toolkit transformation. These instructions ensure consistent, reliable implementation while maintaining backward compatibility and providing comprehensive verification at each step.

## 🚨 Critical Implementation Rules

### MANDATORY Requirements
- ✅ **ENHANCE existing files only** - never create separate package directories
- ✅ **Work within the EXISTING agent-service-toolkit repository**
- ✅ **ADD new functionality to existing `src/agents/agents.py` and `src/service/service.py`**
- ✅ **MAINTAIN 100% backward compatibility** throughout implementation
- ✅ **VERIFY each step** before proceeding to the next
- ✅ **WAIT for user confirmation** after each tool use
- ✅ **NEVER mark anything complete** without running verification commands
- ✅ **STOP after each phase** and request user approval before continuing

### FORBIDDEN Actions
- ❌ **NEVER create new package directories** like `src/agent_service_toolkit/`
- ❌ **NEVER replace existing code** - only add to existing files
- ❌ **NEVER proceed without verification** - all changes must be tested
- ❌ **NEVER skip user confirmation** after tool uses
- ❌ **NEVER continue to next phase** without explicit user approval

## 📋 Startup Protocol

### 1. Environment Assessment
```bash
# Check current state
test -f IMPLEMENTATION_STATE.json && echo "State file exists" || echo "Starting fresh"

# Verify we're in the correct repository
ls -la src/agents/agents.py src/service/service.py

# Check for any existing enhancement
grep -q "AgentService" src/agents/agents.py && echo "⚠️ Already enhanced" || echo "✅ Ready for enhancement"
```

### 2. State File Initialization
If no `IMPLEMENTATION_STATE.json` exists, create it:

```bash
echo '{
  "project_name": "agent-service-toolkit-transformation",
  "started_at": "'$(date -Iseconds)'",
  "current_phase": 1,
  "phases": {},
  "blockers": [],
  "next_actions": ["Begin Phase 1: Enhanced agents.py"]
}' > IMPLEMENTATION_STATE.json
```

### 3. Current Progress Assessment
```bash
# Read current progress
jq -r '.current_phase // 1, .phases | keys[]?' IMPLEMENTATION_STATE.json 2>/dev/null || echo "No phases started yet"

# Check for blockers
jq -r '.blockers[]?' IMPLEMENTATION_STATE.json 2>/dev/null || echo "No blockers"
```

## 🔄 Phase-by-Phase Implementation

### Phase 1: Enhanced agents.py with AgentService Class

#### Step 1.1: Add AgentService Class to agents.py
**Objective**: Add the `AgentService` class to the END of existing `src/agents/agents.py`

**Implementation**:
1. Read current `src/agents/agents.py` content
2. Add the AgentService class and supporting code to the END
3. Update module exports (`__all__`)
4. Verify imports work

**Verification Commands**:
```bash
# Test enhanced agents.py import
cd src && python -c "from agents import AgentService; print('✅ AgentService import successful')"

# Test backward compatibility
cd src && python -c "from agents import get_agent, agents; print('✅ Legacy imports still work')"

# Test basic AgentService instantiation
cd src && python -c "from agents import AgentService; app = AgentService(); print('✅ AgentService created')"
```

#### Step 1.2: Verify Backward Compatibility
**Verification Commands**:
```bash
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

**State Update**:
```bash
jq '.phases["1"] = {
  "name": "Enhanced agents.py with AgentService Class",
  "status": "completed",
  "progress": 100,
  "completed_at": "'$(date -Iseconds)'",
  "steps": {
    "1.1": {"status": "completed", "verified": true},
    "1.2": {"status": "completed", "verified": true}
  }
}' IMPLEMENTATION_STATE.json > tmp.json && mv tmp.json IMPLEMENTATION_STATE.json
```

### Phase 2: Enhanced service.py with AgentService Support

#### Step 2.1: Add Enhanced App Creation Function
**Objective**: Add `create_enhanced_app()` function to `src/service/service.py`

**Implementation**:
1. Add the function BEFORE the existing `app = FastAPI(lifespan=lifespan)` line
2. Include enhanced lifespan management
3. Support both legacy and AgentService agents

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
```

#### Step 2.2: Add Enhanced Agent Resolution
**Objective**: Add `get_agent_with_service()` function for enhanced agent resolution

**Verification Commands**:
```bash
# Verify existing service still works
cd src && python -c "
from service.service import app
print('✅ Legacy service app still available')
"
```

### Phase 3: MCP Integration Support

#### Step 3.1: Create MCP Integration Module
**Objective**: Create `src/agents/mcp_integration.py` for MCP server support

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

### Phase 4: Package Configuration

#### Step 4.1: Update pyproject.toml
**Objective**: Configure pyproject.toml for selective PyPI distribution

**Verification Commands**:
```bash
# Test package build (dry run)
python -m build --wheel --outdir dist/

# Test CLI help
cd src && python -m agents.cli --help
```

### Phase 5: Testing and Verification

#### Step 5.1: Create Core Framework Tests
**Objective**: Create comprehensive tests for the enhanced framework

**Verification Commands**:
```bash
# Run existing tests to ensure no regression
pytest tests/ -v --tb=short

# Run new tests
pytest tests/agents/test_agent_service.py -v
pytest tests/service/test_enhanced_service.py -v
```

### Phase 6: Documentation and Examples

#### Step 6.1: Create Usage Examples
**Objective**: Create documentation and usage examples

**Verification Commands**:
```bash
# Test example
cd examples/enhanced_framework && python main.py &
sleep 2 && curl http://localhost:8000/info && kill %1
```

## 📊 Step Execution Protocol

### Before Starting Any Step
1. **Read Step Requirements** from [IMPLEMENTATION_PHASES.md](IMPLEMENTATION_PHASES.md)
2. **Update State File** to mark step as "in_progress"
3. **Plan Verification** - identify how success will be measured
4. **Check Dependencies** - verify previous steps are complete

### During Step Implementation
1. **Work Incrementally** - make small changes and test frequently
2. **Preserve Existing Code** - only ADD, never REPLACE
3. **Test Each Change** - run verification commands after modifications
4. **Document Issues** - note any problems in IMPLEMENTATION_STATE.json

### After Step Completion
1. **Run ALL Verification Commands** provided in the phase documentation
2. **Wait for User Confirmation** of each tool use result
3. **Update State File** only after verification passes
4. **Request Phase Approval** before proceeding to next phase

## 🔧 Verification Framework

### Verification Types

#### Type A: Automated Verification
- Import statements work without errors
- Unit tests pass
- Commands execute successfully
- Files contain expected content

#### Type B: Manual Verification
- User confirms functionality works as expected
- Visual inspection of outputs
- End-to-end workflow validation

#### Type C: Integration Verification
- Multiple components work together
- Backward compatibility maintained
- No regression in existing functionality

### Mandatory Verification Checklist

Before marking any step complete:

```markdown
## Step Verification Checklist

### Pre-Verification
- [ ] All files mentioned in step have been created/modified
- [ ] No syntax errors in Python files
- [ ] No import errors when testing modules

### Automated Tests
- [ ] Step-specific verification commands pass
- [ ] Existing tests still pass
- [ ] New tests pass (if created)

### Integration Verification
- [ ] No breaking changes to existing functionality
- [ ] Dependencies resolve correctly
- [ ] Performance impact is acceptable

### State Documentation
- [ ] Progress state file updated
- [ ] Verification results logged
- [ ] Any issues documented
```

## 🚨 Error Handling Protocol

### When Verification Fails
1. **DO NOT mark step as complete**
2. **Document failure in IMPLEMENTATION_STATE.json**:
   ```bash
   jq '.blockers += [{
     "step": "X.Y",
     "error": "Description of error",
     "timestamp": "'$(date -Iseconds)'",
     "output": "Error output here"
   }]' IMPLEMENTATION_STATE.json > tmp.json && mv tmp.json IMPLEMENTATION_STATE.json
   ```
3. **Show error output to user**
4. **Propose fix or ask for guidance**
5. **Re-run verification after fix**

### Recovery Commands
```bash
# Reset specific step if needed
jq '.phases["X"].steps["X.Y"].status = "not_started" | .phases["X"].steps["X.Y"].verified = false' IMPLEMENTATION_STATE.json > tmp.json && mv tmp.json IMPLEMENTATION_STATE.json

# Clear blockers after resolution
jq '.blockers = []' IMPLEMENTATION_STATE.json > tmp.json && mv tmp.json IMPLEMENTATION_STATE.json
```

## 📋 Phase Completion Protocol

After completing all steps in a phase, use this template:

```markdown
## Phase X Completion Summary

### What Was Implemented:
- [List specific files created/modified]
- [List functionality added]
- [List verification tests passed]

### Phase Completion Checklist Results:
- [ ] Technical Verification: All steps verified with automated tests
- [ ] Documentation Verification: Code properly documented
- [ ] Compatibility Verification: No breaking changes introduced
- [ ] User Experience Verification: Features work as expected

### Verification Commands Run:
```bash
[Show the actual commands executed and their output]
```

### Next Phase Preview:
Phase Y will implement: [brief description]

**🛑 USER CONFIRMATION REQUIRED:**
Phase X is complete and verified. Please confirm before I proceed to Phase Y.
```

## 🎯 Critical Success Factors

### 1. Incremental Implementation
- Never implement multiple phases at once
- Each step must be verified before proceeding
- Always maintain working state

### 2. Backward Compatibility
- Existing `agents/agents.py` approach continues to work
- All existing tests must pass
- No breaking changes in API

### 3. Comprehensive Verification
- Automated testing at each step
- Manual confirmation when needed
- Integration testing across components

### 4. Clear Communication
- Always wait for user confirmation after tool use
- Provide specific verification commands
- Request explicit approval before phase transitions

## 🔍 Quick Reference Commands

### Environment Check
```bash
# Verify environment
python --version && jq --version && git --version

# Check existing structure
ls -la src/ | head -10

# Read current progress
jq -r '.current_phase // 1, .phases | keys[]?' IMPLEMENTATION_STATE.json 2>/dev/null || echo "No phases started yet"
```

### State Management
```bash
# Create initial state
echo '{"project_name": "agent-service-toolkit-transformation", "started_at": "'$(date -Iseconds)'", "current_phase": 1, "phases": {}}' > IMPLEMENTATION_STATE.json

# Update progress
jq '.phases["1"].status = "completed" | .last_updated = "'$(date -Iseconds)'"' IMPLEMENTATION_STATE.json > tmp.json && mv tmp.json IMPLEMENTATION_STATE.json

# Check for blockers
jq -r '.blockers[]?' IMPLEMENTATION_STATE.json 2>/dev/null || echo "No blockers"
```

### Common Verifications
```bash
# Test basic imports
cd src && python -c "from agents import AgentService; print('✅ Import successful')"

# Test backward compatibility
cd src && python -c "from agents import get_agent; agent = get_agent('research-assistant'); print('✅ Legacy works')"

# Run existing tests
pytest tests/ -k "test_" --tb=short
```

## 📈 Progress Tracking Template

```json
{
  "project_name": "agent-service-toolkit-transformation",
  "started_at": "2024-01-01T10:00:00Z",
  "last_updated": "2024-01-01T14:30:00Z",
  "current_phase": 1,
  "overall_progress": 16,
  "phases": {
    "1": {
      "name": "Enhanced agents.py with AgentService Class",
      "status": "in_progress",
      "progress": 50,
      "started_at": "2024-01-01T10:00:00Z",
      "steps": {
        "1.1": {"status": "completed", "verified": true},
        "1.2": {"status": "in_progress", "verified": false}
      }
    }
  },
  "verification_log": [
    {
      "step": "1.1",
      "timestamp": "2024-01-01T10:30:00Z",
      "method": "automated",
      "result": "success",
      "command": "cd src && python -c \"from agents import AgentService; print('✅ Import successful')\""
    }
  ],
  "blockers": [],
  "next_actions": [
    "Complete step 1.2: Verify backward compatibility",
    "Run comprehensive integration tests",
    "Request user approval for Phase 2"
  ]
}
```

---

## 🚀 Simple Startup Command

**For immediate use:**

```
Follow the LLM Coding Assistant Instructions in docs/transformation/LLM_ASSISTANT_INSTRUCTIONS.md to implement the Agent Service Toolkit transformation. Start by checking the current implementation state and begin with Phase 1.
```

---

*These instructions provide comprehensive guidance for LLM assistants to reliably implement the Agent Service Toolkit transformation while maintaining quality, compatibility, and verification standards.*
