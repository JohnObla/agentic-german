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

def test_get_current_word_missing_learned_file():
    """Test when learned words file doesn't exist"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(all_words, f2)
        all_file = f2.name
    
    # Use a non-existent file path for learned words
    non_existent_learned = "/tmp/non_existent_learned.json"
    result = get_current_word(non_existent_learned, all_file)
    assert result.word == 'spieler'
    os.unlink(all_file)

def test_get_current_word_missing_wordlist_file():
    """Test when wordlist file doesn't exist"""
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump(learned, f1)
        learned_file = f1.name
    
    # Use a non-existent file path for wordlist
    non_existent_wordlist = "/tmp/non_existent_wordlist.json"
    result = get_current_word(learned_file, non_existent_wordlist)
    assert result is None
    os.unlink(learned_file)

def test_get_current_word_empty_learned_file():
    """Test when learned words file is empty"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write empty content to learned file
        f1.write("")
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result.word == 'spieler'
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_empty_wordlist_file():
    """Test when wordlist file is empty"""
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        # Write empty content to wordlist file
        f2.write("")
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result is None
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_malformed_learned_json():
    """Test when learned words file has malformed JSON"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write malformed JSON to learned file
        f1.write("{invalid json")
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result.word == 'spieler'
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_malformed_wordlist_json():
    """Test when wordlist file has malformed JSON"""
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        # Write malformed JSON to wordlist file
        f2.write("{invalid json")
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result is None
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_non_dict_learned():
    """Test when learned words file contains non-dict data"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write list instead of dict to learned file
        json.dump(["not", "a", "dict"], f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result.word == 'spieler'
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_non_list_wordlist():
    """Test when wordlist file contains non-list data"""
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        # Write dict instead of list to wordlist file
        json.dump({"not": "a list"}, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result is None
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_malformed_word_entries():
    """Test when wordlist contains malformed word entries"""
    learned = {}
    all_words = [
        "not a dict",  # Invalid entry
        {"word": "missing_fields"},  # Missing required fields
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}  # Valid entry
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result.word == 'spieler'  # Should skip malformed entries and return valid one
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_current_word_all_entries_malformed():
    """Test when all wordlist entries are malformed"""
    learned = {}
    all_words = [
        "not a dict",
        {"missing": "word field"},
        {"word": "missing_required_fields"}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    result = get_current_word(learned_file, all_file)
    assert result is None  # Should return None when no valid entries exist
    os.unlink(learned_file)
    os.unlink(all_file) 