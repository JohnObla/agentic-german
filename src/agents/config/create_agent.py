from pydantic import BaseModel
from autogen import ConversableAgent, register_function
from typing import List, Callable, Type, Optional
from .termination_message import TERMINATION_MSG, transform_response_format_with_termination
from .llm_config import make_llm_config
from .schemas import AgentFactoryReturn, AgentFactoryProtocol

def create_agent(
    name: str,
    system_message: str,
    default_functions: Optional[List[Callable]] = None,
    default_response_format: Optional[Type[BaseModel]] = None
) -> AgentFactoryProtocol:
    """
    Higher-order function that creates an agent factory function.
    Args:
        name: The agent name
        system_message: The agent's system message
        default_functions: Default function callables (optional)
        default_response_format: Default response format for the agent (optional, must inherit from BaseModel)
    Returns:
        A function that creates an agent with a required executor, and optional function callables and response_format.
    """
    def agent_factory(
        executor,
        *,
        functions: Optional[List[Callable]] = None,
        response_format: Optional[Type[BaseModel]] = None
    ) -> AgentFactoryReturn:
        """Create an agent with a required executor, and optional function callables and response format. Returns a dict with 'sender' (executor) and 'recipient' (agent)."""
        if executor is None:
            raise ValueError("executor is required and must be a UserProxyAgent instance.")
        functions = functions if functions is not None else default_functions
        
        # Transform response_format to include termination_msg if provided
        final_response_format = response_format if response_format is not None else default_response_format
        if final_response_format is not None:
            final_response_format = transform_response_format_with_termination(final_response_format)

        base_prompt = f"""
        Additionally, add the text {TERMINATION_MSG} to your output if any of these conditions are met:
        1. You want feedback from the user.
        2. You want to ask the user something.
        3. You have finished your task.
        
        IMPORTANT: When you ask the user for any input (like a URL, confirmation, or any information), you MUST include {TERMINATION_MSG} immediately in the same message where you ask for the input.
        Do not wait for a response before including the termination message.
        """
        final_system_message = system_message + "\n\n" + base_prompt

        llm_config = make_llm_config(final_response_format)
        agent = ConversableAgent(
            name=name,
            system_message=final_system_message,
            llm_config=llm_config,
        )

        # Register each function using register_function, passing executor (now required)
        if functions:
            for func in functions:
                register_function(f=func, description=func.__doc__, caller=agent, executor=executor)

        return {"sender": executor, "recipient": agent}
    return agent_factory 