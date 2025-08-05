from typing import List, Callable, Type, TypedDict, Optional, Protocol
from autogen import UserProxyAgent, ConversableAgent

# TypedDict for agent_factory return value
class AgentFactoryReturn(TypedDict):
    sender: UserProxyAgent
    recipient: ConversableAgent

# Protocol for agent factory with keyword-only arguments
class AgentFactoryProtocol(Protocol):
    def __call__(
        self,
        executor: UserProxyAgent,
        *,
        functions: Optional[List[Callable]] = None,
        response_format: Optional[Type] = None
    ) -> AgentFactoryReturn: ... 