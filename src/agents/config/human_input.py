from autogen import UserProxyAgent
from .termination_message import is_termination_msg

human_input = UserProxyAgent(
    name="human_input",
    human_input_mode="TERMINATE",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)
"""
human_input: A UserProxyAgent configured for manual (human) input mode. Use this agent when you want human interaction in the loop.
"""

no_human_input = UserProxyAgent(
    name="no_human_input",
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg,
)
"""
no_human_input: A UserProxyAgent configured for fully automated tool execution (no human input). Use this agent for autonomous flows.
""" 