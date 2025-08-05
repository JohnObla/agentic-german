from ..functions import get_current_word, get_next_word_from_current_word
from .config import create_agent

system_message = """
You are an assistant that retrieves items when instructed.
"""
create_get_item_agent = create_agent(
    name="get_item_agent",
    system_message=system_message,
    default_functions=[get_current_word, get_next_word_from_current_word],
) 
