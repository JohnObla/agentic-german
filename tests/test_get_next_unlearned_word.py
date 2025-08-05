import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.functions import get_current_word

def test_get_current_word_basic():
    # Setup temp files
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    all_words = [
        {"word": "sicherheit", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "security", "romanization": "sicherheit", "example_sentence_native": "Die Sicherheit ist wichtig.", "example_sentence_english": "Security is important.", "frequency_index": 1},
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    result = get_current_word(learned_file, all_file)
    assert result.word == 'spieler'
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_none():
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}, "spieler": {"word": "spieler", "frequency_index": 2}}
    all_words = [
        {"word": "sicherheit", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "security", "romanization": "sicherheit", "example_sentence_native": "Die Sicherheit ist wichtig.", "example_sentence_english": "Security is important.", "frequency_index": 1},
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    result = get_current_word(learned_file, all_file)
    assert result is None
    os.unlink(learned_file)
    os.unlink(all_file) 