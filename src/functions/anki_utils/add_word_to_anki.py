import subprocess
from typing import List, Optional, Callable, Dict
from src.schemas import AnkiWordWithPronunciation


def _execute_apy_command(model: str, fields: List[str], word: str) -> str:
    """
    Execute the apy command with the given model and fields.
    
    Args:
        model: The Anki model name
        fields: List of field values in correct order
        word: The word being added (for logging/error messages)
        
    Returns:
        Success message if successful
        
    Raises:
        subprocess.CalledProcessError: If apy command fails
    """
    cmd = ["apy", "add-single", f"--model={model}"] + fields
    
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(f"Successfully added word '{word}' to Anki")
    return result.stdout


def _format_image_tag(image_filename: Optional[str]) -> str:
    """Format image filename as HTML tag or return empty string."""
    return f'<img src="{image_filename}">' if image_filename else ""


def _value_or_empty_string(value: Optional[str]) -> str:
    """Convert None values to empty strings for Anki fields."""
    return value or ""


def _extract_noun_fields(anki_word: AnkiWordWithPronunciation, image_filename: str) -> List[str]:
    """Extract fields for Deutsche Nomen model."""
    noun_fields = anki_word.noun
    noun_pronunciation = anki_word.noun_pronunciation
    
    return [
        noun_fields.singular,
        _value_or_empty_string(noun_fields.plural),
        _value_or_empty_string(noun_pronunciation.singular if noun_pronunciation else None),
        _value_or_empty_string(noun_pronunciation.plural if noun_pronunciation else None),
        _format_image_tag(image_filename)
    ]


def _extract_adjective_fields(anki_word: AnkiWordWithPronunciation, image_filename: str) -> List[str]:
    """Extract fields for Deutsche Adjektive model."""
    adj_fields = anki_word.adjective
    adj_pronunciation = anki_word.adjective_pronunciation
    
    return [
        adj_fields.positive,
        _value_or_empty_string(adj_fields.comparative),
        _value_or_empty_string(adj_fields.superlative),
        _value_or_empty_string(adj_pronunciation.positive if adj_pronunciation else None),
        _value_or_empty_string(adj_pronunciation.comparative if adj_pronunciation else None),
        _value_or_empty_string(adj_pronunciation.superlative if adj_pronunciation else None),
        _format_image_tag(image_filename)
    ]


def _extract_verb_fields(anki_word: AnkiWordWithPronunciation, image_filename: str) -> List[str]:
    """Extract fields for Deutsche Verben model."""
    verb_fields = anki_word.verb
    verb_pronunciation = anki_word.verb_pronunciation
    
    return [
        verb_fields.infinitive,
        verb_fields.present,
        verb_fields.written_past,
        verb_fields.spoken_past,
        _value_or_empty_string(verb_pronunciation.infinitive if verb_pronunciation else None),
        _value_or_empty_string(verb_pronunciation.present if verb_pronunciation else None),
        _value_or_empty_string(verb_pronunciation.written_past if verb_pronunciation else None),
        _value_or_empty_string(verb_pronunciation.spoken_past if verb_pronunciation else None),
        _format_image_tag(image_filename)
    ]


def _extract_adverb_fields(anki_word: AnkiWordWithPronunciation, image_filename: str) -> List[str]:
    """Extract fields for Deutsche Vokabeln model."""
    adverb_fields = anki_word.adverb
    adverb_pronunciation = anki_word.adverb_pronunciation
    
    return [
        adverb_fields.cloze_example_sentence,
        _value_or_empty_string(adverb_pronunciation.example_sentence if adverb_pronunciation else None),
        _format_image_tag(image_filename)
    ]


# Mapping of word types to their model names and field extraction functions
WORD_TYPE_HANDLERS: Dict[str, tuple[str, Callable]] = {
    "noun": ("Deutsche Nomen", _extract_noun_fields),
    "adjective": ("Deutsche Adjektive", _extract_adjective_fields),
    "verb": ("Deutsche Verben", _extract_verb_fields),
    "adverb": ("Deutsche Vokabeln", _extract_adverb_fields),
}


def add_word_to_anki(anki_word: AnkiWordWithPronunciation, image_filename: str) -> str:
    """
    Add a word to Anki using the apy command.
    
    Args:
        word: The Word object containing word information
        anki_word: The AnkiWordWithPronunciation object with word forms and sound recordings
        image_filename: The filename of the image for the card
        
    Returns:
        Success message if successful, error message if failure
    """
    try:
        word_type = anki_word.word_type
        
        # Check if word type is supported
        if word_type not in WORD_TYPE_HANDLERS:
            error_msg = f"Unsupported word type: {word_type}"
            print(error_msg)
            return error_msg
        
        # Get model name and field extractor for this word type
        model_name, field_extractor = WORD_TYPE_HANDLERS[word_type]
        
        # Check if field data exists for this word type
        word_data = getattr(anki_word, word_type, None)
        if not word_data:
            error_msg = f"No field data found for {word_type}."
            print(error_msg)
            return error_msg
        
        # Extract fields and execute command
        fields = field_extractor(anki_word, image_filename)
        return _execute_apy_command(model_name, fields, anki_word.word)
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Error adding word to Anki: {e}\nCommand output: {e.stdout}\nError output: {e.stderr}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error adding word to Anki: {e}"
        print(error_msg)
        return error_msg 