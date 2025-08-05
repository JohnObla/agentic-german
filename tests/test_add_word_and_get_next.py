import json
import os
import tempfile

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