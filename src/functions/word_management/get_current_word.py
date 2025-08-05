import json
import os
from typing import Optional
from src.schemas import Word

def get_current_word(
    learned_path: str = 'src/data/already_learned_words.json',
    wordlist_path: str = 'src/data/german-word-list.json',
) -> Optional[Word]:
    """
    Get the next unlearned word from the word list.

    Args:
        learned_path: Path to the JSON file containing already learned words (default: 'src/data/already_learned_words.json').
        wordlist_path: Path to the JSON file containing the full word list (default: 'src/data/german-word-list.json').

    Returns:
        The next unlearned Word object, or None if all words have been learned or no words exist.
    """
    # Load learned words with error handling
    learned_words = set()
    if os.path.exists(learned_path):
        try:
            with open(learned_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    learned_data = json.loads(content)
                    if isinstance(learned_data, dict):
                        learned_words = set(learned_data.keys())
        except (json.JSONDecodeError, IOError):
            # If file is malformed or can't be read, start with empty set
            learned_words = set()

    # Load all words with error handling
    if not os.path.exists(wordlist_path):
        return None
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:  # Empty file
                return None
            all_words = json.loads(content)
            if not isinstance(all_words, list):
                return None
    except (json.JSONDecodeError, IOError):
        # If file is malformed or can't be read, return None
        return None

    # Find first unlearned word
    for entry in all_words:
        if isinstance(entry, dict) and 'word' in entry and entry['word'] not in learned_words:
            try:
                return Word(**entry)
            except (TypeError, ValueError):
                # Skip malformed word entries
                continue
    
    return None 