from ..schemas import AnkiWordWithPronunciation
from .config import create_agent

system_message = """
You are a German language assistant that generates pronunciation data on German words.
You will receive information describing a German word.
Keep the original context intact.

Use these rules to generate the pronunciations:

NOUN:
    singular_pronunciation: copy the singular field exactly
    plural_pronunciation: copy the plural field exactly

VERB:
    infinitive_pronunciation: copy the infinitive field exactly
    present_pronunciation: copy the present field and prepend "er/sie/es" to the pronunciation
        Example: "setzt" → "er/sie/es setzt"
    written_past_pronunciation: copy the written_past field and prepend "er/sie/es" to the pronunciation
        Example: "setzte" → "er/sie/es setzte"
    spoken_past_pronunciation: copy the spoken_past field and prepend "er/sie/es" to the pronunciation
        Example: "hat gesetzt" → "er/sie/es hat gesetzt"


ADJECTIVE:
    positive_pronunciation: copy the positive field exactly
    comparative_pronunciation: copy the comparative field exactly
    superlative_pronunciation: copy the superlative field exactly

ADVERB:
    example_sentence_pronunciation: copy the example_sentence field exactly
"""

create_word_pronunciation_agent = create_agent(
    name="word_pronunciation_agent",
    system_message=system_message,
    default_response_format=AnkiWordWithPronunciation
) 