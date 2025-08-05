import json
import os
from typing import Optional
from src.schemas import Word
from .get_current_word import get_current_word

def get_next_word_from_current_word(
    word_obj: Word,
    learned_path: str = 'src/data/already_learned_words.json',
    wordlist_path: str = 'src/data/german-word-list.json',
) -> Optional[Word]:
    """
    Mark the given word as learned and return the next unlearned word.

    Args:
        word_obj: The Word object to mark as learned.
        learned_path: Path to the JSON file containing already learned words (default: 'src/data/already_learned_words.json').
        wordlist_path: Path to the JSON file containing the full word list (default: 'src/data/german-word-list.json').

    Returns:
        The next unlearned Word object, or None if all words have been learned or no words exist.
    """
    # Load current learned words with error handling
    learned = {}
    if os.path.exists(learned_path):
        try:
            with open(learned_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    learned_data = json.loads(content)
                    if isinstance(learned_data, dict):
                        learned = learned_data
        except (json.JSONDecodeError, IOError):
            # If file is malformed or can't be read, start with empty dict
            learned = {}
    
    # Add the new word
    learned[word_obj.word] = word_obj.model_dump()
    
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(learned_path), exist_ok=True)
    
    # Save updated learned words
    try:
        with open(learned_path, 'w', encoding='utf-8') as f:
            json.dump(learned, f, indent=2, ensure_ascii=False)
    except IOError:
        # If we can't save, we can still try to return the next word
        pass
    
    # Return the next unlearned word
    return get_current_word(learned_path, wordlist_path) 