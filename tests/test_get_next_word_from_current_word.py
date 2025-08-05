import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

from src.functions import get_next_word_from_current_word
from src.schemas import Word

def test_get_next_word_from_current_word_basic():
    learned = {"sicherheit": {"word": "sicherheit", "frequency_index": 1}}
    all_words = [
        {"word": "sicherheit", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "security", "romanization": "sicherheit", "example_sentence_native": "Die Sicherheit ist wichtig.", "example_sentence_english": "Security is important.", "frequency_index": 1},
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(learned, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    # Add 'spieler' and get next
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    # Check that the word was added
    with open(learned_file, 'r') as f:
        updated = json.load(f)
    assert "spieler" in updated
    assert result.word == 'drauf'
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_from_current_word_none():
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
    # Add a word when all are learned
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    assert result is None
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_missing_learned_file():
    """Test when learned words file doesn't exist initially"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(all_words, f2)
        all_file = f2.name
    
    # Use a non-existent file path for learned words
    with tempfile.TemporaryDirectory() as tmpdir:
        non_existent_learned = os.path.join(tmpdir, "new_learned.json")
        new_word = Word(
            word="spieler",
            useful_for_flashcard=True,
            cefr_level="A2",
            english_translation="player",
            romanization="spieler",
            example_sentence_native="Der Spieler hat ein Tor geschossen.",
            example_sentence_english="The player scored a goal.",
            frequency_index=2
        )
        result = get_next_word_from_current_word(new_word, non_existent_learned, all_file)
        
        # Check that the learned file was created and word was added
        assert os.path.exists(non_existent_learned)
        with open(non_existent_learned, 'r') as f:
            learned_data = json.load(f)
        assert "spieler" in learned_data
        assert result.word == 'drauf'
    
    os.unlink(all_file)

def test_get_next_word_missing_wordlist_file():
    """Test when wordlist file doesn't exist"""
    with tempfile.TemporaryDirectory() as tmpdir:
        learned_file = os.path.join(tmpdir, "learned.json")
        non_existent_wordlist = "/tmp/non_existent_wordlist.json"
        
        new_word = Word(
            word="spieler",
            useful_for_flashcard=True,
            cefr_level="A2",
            english_translation="player",
            romanization="spieler",
            example_sentence_native="Der Spieler hat ein Tor geschossen.",
            example_sentence_english="The player scored a goal.",
            frequency_index=2
        )
        result = get_next_word_from_current_word(new_word, learned_file, non_existent_wordlist)
        
        # Check that the word was still saved to learned file
        assert os.path.exists(learned_file)
        with open(learned_file, 'r') as f:
            learned_data = json.load(f)
        assert "spieler" in learned_data
        assert result is None

def test_get_next_word_empty_learned_file():
    """Test when learned words file is empty"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write empty content to learned file
        f1.write("")
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    
    # Check that the word was added
    with open(learned_file, 'r') as f:
        learned_data = json.load(f)
    assert "spieler" in learned_data
    assert result.word == 'drauf'
    
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_empty_wordlist_file():
    """Test when wordlist file is empty"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write empty content to wordlist file
        f1.write("{}")
        f2.write("")
        learned_file = f1.name
        all_file = f2.name
    
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    
    # Check that the word was still saved
    with open(learned_file, 'r') as f:
        learned_data = json.load(f)
    assert "spieler" in learned_data
    assert result is None
    
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_malformed_learned_json():
    """Test when learned words file has malformed JSON"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write malformed JSON to learned file
        f1.write("{invalid json")
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    
    # Check that the word was added (file should be overwritten with valid JSON)
    with open(learned_file, 'r') as f:
        learned_data = json.load(f)
    assert "spieler" in learned_data
    assert result.word == 'drauf'
    
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_non_dict_learned():
    """Test when learned words file contains non-dict data"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        # Write list instead of dict to learned file
        json.dump(["not", "a", "dict"], f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    
    # Check that the word was added (should start fresh with empty dict)
    with open(learned_file, 'r') as f:
        learned_data = json.load(f)
    assert "spieler" in learned_data
    assert result.word == 'drauf'
    
    os.unlink(learned_file)
    os.unlink(all_file)

def test_get_next_word_directory_creation():
    """Test that parent directories are created when they don't exist"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(all_words, f2)
        all_file = f2.name
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a nested path that doesn't exist
        nested_learned_file = os.path.join(tmpdir, "deep", "nested", "path", "learned.json")
        
        new_word = Word(
            word="spieler",
            useful_for_flashcard=True,
            cefr_level="A2",
            english_translation="player",
            romanization="spieler",
            example_sentence_native="Der Spieler hat ein Tor geschossen.",
            example_sentence_english="The player scored a goal.",
            frequency_index=2
        )
        result = get_next_word_from_current_word(new_word, nested_learned_file, all_file)
        
        # Check that directories were created and file was saved
        assert os.path.exists(nested_learned_file)
        with open(nested_learned_file, 'r') as f:
            learned_data = json.load(f)
        assert "spieler" in learned_data
        assert result is None  # No more words
    
    os.unlink(all_file)

def test_get_next_word_save_failure_handling():
    """Test graceful handling when save operation fails"""
    all_words = [
        {"word": "spieler", "useful_for_flashcard": True, "cefr_level": "A2", "english_translation": "player", "romanization": "spieler", "example_sentence_native": "Der Spieler spielt gut.", "example_sentence_english": "The player plays well.", "frequency_index": 2},
        {"word": "drauf", "useful_for_flashcard": True, "cefr_level": "B1", "english_translation": "on it", "romanization": "drauf", "example_sentence_native": "Leg es drauf.", "example_sentence_english": "Put it on it.", "frequency_index": 3}
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({}, f1)
        json.dump(all_words, f2)
        learned_file = f1.name
        all_file = f2.name
    
    # Make the learned file read-only to cause save failure
    os.chmod(learned_file, 0o444)
    
    new_word = Word(
        word="spieler",
        useful_for_flashcard=True,
        cefr_level="A2",
        english_translation="player",
        romanization="spieler",
        example_sentence_native="Der Spieler hat ein Tor geschossen.",
        example_sentence_english="The player scored a goal.",
        frequency_index=2
    )
    
    # Function should still return a word even if save fails
    # Since save failed, learned file is unchanged, so it should return the first word "spieler"
    result = get_next_word_from_current_word(new_word, learned_file, all_file)
    assert result.word == 'spieler'  # Since save failed, learned file is still empty
    
    # Restore permissions and clean up
    os.chmod(learned_file, 0o644)
    os.unlink(learned_file)
    os.unlink(all_file) 