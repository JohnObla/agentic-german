from ..functions import process_word_pronunciation_sync
from ..schemas import AnkiWordWithPronunciation
from .config import create_agent

system_message = """
You are a dictation agent that creates voice recordings for German word pronunciations.

1. Get the pronunciation information from the previous agent.
2. Use the pronunciation information to create voice recordings for the words and save them as MP3 files.
3. Override the pronunciation information with the MP3 files.
"""

create_dictation_agent = create_agent(
    name="dictation_agent",
    system_message=system_message,
    default_functions=[process_word_pronunciation_sync],
    default_response_format=AnkiWordWithPronunciation
) 