from typing import Type
from pydantic import BaseModel
from src.schemas import AddTerminationMsg

TERMINATION_MSG = "***TERMINATION_MSG***"

def is_termination_msg(obj):
    content = obj.get("content")
    return TERMINATION_MSG in content if content else False

def transform_response_format_with_termination(response_format: Type[BaseModel]) -> Type[BaseModel]:
    """
    Transform a response format class to include a termination_msg field.
    Creates a new class that inherits from both the original class and AddTerminationMsg.
    """
    
    # Create a new class that inherits from both the original class and AddTerminationMsg
    class TransformedResponseFormat(response_format, AddTerminationMsg):
        pass
    
    return TransformedResponseFormat 