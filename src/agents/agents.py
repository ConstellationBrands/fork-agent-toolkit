import logging
from collections.abc import Callable
from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel

from agents.bg_task_agent.bg_task_agent import bg_task_agent
from agents.chatbot import chatbot
from agents.command_agent import command_agent
from agents.interrupt_agent import interrupt_agent
from agents.knowledge_base_agent import kb_agent
from agents.langgraph_supervisor_agent import langgraph_supervisor_agent
from agents.rag_assistant import rag_assistant
from agents.research_assistant import research_assistant
from schema import AgentInfo

DEFAULT_AGENT = "research-assistant"

# Type alias to handle LangGraph's different agent patterns
# - @entrypoint functions return Pregel
# - StateGraph().compile() returns CompiledStateGraph
AgentGraph = CompiledStateGraph | Pregel


@dataclass
class Agent:
    description: str
    graph: AgentGraph


agents: dict[str, Agent] = {
    "chatbot": Agent(description="A simple chatbot.", graph=chatbot),
    "research-assistant": Agent(
        description="A research assistant with web search and calculator.", graph=research_assistant
    ),
    "rag-assistant": Agent(
        description="A RAG assistant with access to information in a database.", graph=rag_assistant
    ),
    "command-agent": Agent(description="A command agent.", graph=command_agent),
    "bg-task-agent": Agent(description="A background task agent.", graph=bg_task_agent),
    "langgraph-supervisor-agent": Agent(
        description="A langgraph supervisor agent", graph=langgraph_supervisor_agent
    ),
    "interrupt-agent": Agent(description="An agent the uses interrupts.", graph=interrupt_agent),
    "knowledge-base-agent": Agent(
        description="A retrieval-augmented generation agent using Amazon Bedrock Knowledge Base",
        graph=kb_agent,
    ),
}


def get_agent(agent_id: str) -> AgentGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]


# Enhanced Framework - AgentService Class and Supporting Functions
# This section adds FastAPI-style functionality while maintaining 100% backward compatibility

# Type alias for agent factory functions
AgentFactory = Callable[[], AgentGraph]

logger = logging.getLogger(__name__)


class AgentService:
    """
    FastAPI-style service for registering and managing agents.

    This class provides a decorator-based API similar to FastAPI routes,
    allowing developers to register agents using @app.agent() decorators.
    """

    def __init__(self, checkpointer=None, store=None, mcp_servers: list[str] | None = None):
        """
        Initialize the AgentService.

        Args:
            checkpointer: Optional checkpointer for agent persistence
            store: Optional store for agent data
            mcp_servers: Optional list of MCP server configurations
        """
        self._agents: dict[str, AgentFactory] = {}
        self._agent_descriptions: dict[str, str] = {}
        self._checkpointer = checkpointer
        self._store = store
        self._mcp_servers = mcp_servers or []

    def agent(self, name: str, description: str = ""):
        """
        Decorator for registering agent factory functions.

        Usage:
            @app.agent("my-bot", description="My custom bot")
            def create_my_bot():
                return compiled_langgraph_agent

        Args:
            name: Unique name for the agent
            description: Human-readable description of the agent
        """

        def decorator(factory_func: AgentFactory) -> AgentFactory:
            if name in self._agents:
                logger.warning(f"Agent '{name}' is being overridden")

            self._agents[name] = factory_func
            self._agent_descriptions[name] = description
            logger.info(f"Registered agent: {name}")
            return factory_func

        return decorator

    def get_agent(self, agent_id: str) -> AgentGraph:
        """Get an agent by ID from the AgentService registry."""
        if agent_id not in self._agents:
            raise KeyError(f"Agent '{agent_id}' not found in AgentService registry")

        factory = self._agents[agent_id]
        return factory()

    def get_agent_info(self) -> list[AgentInfo]:
        """Get information about all registered agents."""
        return [
            AgentInfo(key=agent_id, description=description)
            for agent_id, description in self._agent_descriptions.items()
        ]

    def create_app(self):
        """
        Create a FastAPI application with this AgentService instance.

        This method imports and calls the enhanced service creation function
        from the service module.
        """
        from service.service import create_enhanced_app

        return create_enhanced_app(self)

    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        """
        Run the AgentService using uvicorn.

        Args:
            host: Host to bind to
            port: Port to bind to
            reload: Enable auto-reload for development
        """
        try:
            import uvicorn

            if reload:
                # When reload=True, uvicorn needs an import string
                # Disable reload and warn user about the limitation
                logger.warning(
                    "Auto-reload is not supported when running AgentService directly. "
                    "Use CLI with 'python -m agents.cli run app.py:app --reload' for reload support."
                )
                reload = False

            app = self.create_app()

            uvicorn.run(
                app,
                host=host,
                port=port,
                reload=reload,
                log_level="info",
            )
        except ImportError:
            logger.error(
                "uvicorn is required to run the AgentService. Install with: pip install uvicorn"
            )
            raise
        except Exception as e:
            logger.error(f"Failed to run AgentService: {e}")
            raise


def get_agent_enhanced(agent_id: str) -> AgentGraph:
    """
    Enhanced agent retrieval that checks AgentService registries first,
    then falls back to legacy agents dictionary.

    This function maintains backward compatibility while enabling
    enhanced functionality when available.
    """
    # Note: In a full implementation, this would check if there's an
    # active AgentService instance. For now, it falls back to legacy.
    return get_agent(agent_id)


def get_all_agent_info_enhanced() -> list[AgentInfo]:
    """
    Enhanced agent info retrieval that combines information from
    both legacy agents and any active AgentService instances.
    """
    # Start with legacy agents
    all_info = get_all_agent_info()

    # Note: In a full implementation, this would also include
    # agents from any active AgentService instances.

    return all_info


# Update __all__ to include new functionality
__all__ = [
    "DEFAULT_AGENT",
    "AgentGraph",
    "Agent",
    "agents",
    "get_agent",
    "get_all_agent_info",
    "AgentService",
    "AgentFactory",
    "get_agent_enhanced",
    "get_all_agent_info_enhanced",
]
