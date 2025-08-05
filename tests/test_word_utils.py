import json
import os
import tempfile
import shutil
import pytest
from unittest.mock import patch, MagicMock

from src.functions import get_current_word, get_next_word_from_current_word
from src.schemas import Word


class TestWordUtils:
    @pytest.fixture
    def temp_files(self):
        """Create temporary files for testing"""
        # Create temporary learned words file
        learned_words = {
            "sicherheit": {
                "word": "sicherheit",
                "useful_for_flashcard": True,
                "cefr_level": "B1",
                "english_translation": "security, safety",
                "romanization": "sicherheit",
                "example_sentence_native": "Die Sicherheit der Daten ist sehr wichtig.",
                "example_sentence_english": "The security of the data is very important.",
                "frequency_index": 1
            }
        }
        
        # Create temporary german word list
        german_words = [
            {
                "word": "sicherheit",
                "useful_for_flashcard": True,
                "cefr_level": "B1",
                "english_translation": "security, safety",
                "romanization": "sicherheit",
                "example_sentence_native": "Die Sicherheit der Daten ist sehr wichtig.",
                "example_sentence_english": "The security of the data is very important.",
                "frequency_index": 1
            },
            {
                "word": "spieler",
                "useful_for_flashcard": True,
                "cefr_level": "A2",
                "english_translation": "player",
                "romanization": "spieler",
                "example_sentence_native": "Der Spieler hat ein Tor geschossen.",
                "example_sentence_english": "The player scored a goal.",
                "frequency_index": 2
            },
            {
                "word": "drauf",
                "useful_for_flashcard": True,
                "cefr_level": "B1",
                "english_translation": "on it, on top of it",
                "romanization": "drauf",
                "example_sentence_native": "Leg das Buch bitte da drauf.",
                "example_sentence_english": "Please put the book on it.",
                "frequency_index": 3
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
            
            json.dump(learned_words, f1, indent=2, ensure_ascii=False)
            json.dump(german_words, f2, indent=2, ensure_ascii=False)
            
            learned_file = f1.name
            german_file = f2.name
        
        yield learned_file, german_file
        
        # Cleanup
        os.unlink(learned_file)
        os.unlink(german_file)
    
    def test_get_current_word(self, temp_files):
        """Test getting the current word"""
        learned_file, german_file = temp_files
        result = get_current_word(learned_file, german_file)
        assert result is not None
        assert result.word == 'spieler'
        assert result.english_translation == 'player'
        assert result.frequency_index == 2
    
    def test_get_current_word_all_learned(self, temp_files):
        """Test when all words are learned"""
        learned_file, german_file = temp_files
        # Update learned words to include all words
        all_learned = {
            "sicherheit": {"word": "sicherheit", "frequency_index": 1},
            "spieler": {"word": "spieler", "frequency_index": 2},
            "drauf": {"word": "drauf", "frequency_index": 3}
        }
        with open(learned_file, 'w', encoding='utf-8') as f:
            json.dump(all_learned, f, indent=2, ensure_ascii=False)
        result = get_current_word(learned_file, german_file)
        assert result is None
    
    def test_get_next_word_from_current_word(self, temp_files):
        """Test adding a word and getting the next one"""
        learned_file, german_file = temp_files
        # Word object to add
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
        result = get_next_word_from_current_word(new_word, learned_file, german_file)
        # Check that the word was added to learned words
        with open(learned_file, 'r', encoding='utf-8') as f:
            updated_learned = json.load(f)
        assert "spieler" in updated_learned
        assert updated_learned["spieler"]["word"] == "spieler"
        assert updated_learned["spieler"]["english_translation"] == "player"
        # Check that the next word is returned (drauf)
        assert result is not None
        assert result.word == 'drauf'
        assert result.english_translation == 'on it, on top of it'
        assert result.frequency_index == 3
    
    def test_get_next_word_from_current_word_no_more_words(self, temp_files):
        """Test adding a word when no more words are available"""
        learned_file, german_file = temp_files
        # Update learned words to include all but one word
        almost_all_learned = {
            "sicherheit": {"word": "sicherheit", "frequency_index": 1},
            "spieler": {"word": "spieler", "frequency_index": 2}
        }
        with open(learned_file, 'w', encoding='utf-8') as f:
            json.dump(almost_all_learned, f, indent=2, ensure_ascii=False)
        # Add the last word
        last_word = Word(
            word="drauf",
            useful_for_flashcard=True,
            cefr_level="B1",
            english_translation="on it, on top of it",
            romanization="drauf",
            example_sentence_native="Leg das Buch bitte da drauf.",
            example_sentence_english="Please put the book on it.",
            frequency_index=3
        )
        result = get_next_word_from_current_word(last_word, learned_file, german_file)
        # Check that the word was added
        with open(learned_file, 'r', encoding='utf-8') as f:
            updated_learned = json.load(f)
        assert "drauf" in updated_learned
        # Check that no more words are available
        assert result is None 