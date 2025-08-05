from ..functions import add_word_to_anki
from .config import create_agent
from ..schemas import AnkiResponse

system_message = """
You are an Anki agent that adds German words to Anki flashcards.

Your task is to:
1. Receive Word Data: You will be provided with information containing word information and sound recordings.
2. Add to Anki: Use the correct tool to add the word to Anki with all its associated data (pronunciations, images, etc.).
3. Return Result: Return the result that was returned by the tool.
"""

create_anki_agent = create_agent(
    name="anki_agent",
    system_message=system_message,
    default_functions=[add_word_to_anki],
    default_response_format=AnkiResponse
) 