import asyncio
from typing import Dict, List, Optional
from src.schemas import AnkiWordWithPronunciation
from .text_to_speech_narakeet import text_to_speech_narakeet
from .save_audio_data import save_audio_data

# Pronunciation fields mapping for each word type based on the pronunciation agent rules
PRONUNCIATION_FIELDS = {
    'noun': ['singular', 'plural'],
    'verb': ['infinitive', 'present', 'written_past', 'spoken_past'],
    'adjective': ['positive', 'comparative', 'superlative'],
    'adverb': ['adverb', 'example_sentence', 'cloze_example_sentence']
}

def _generate_title(word: str, word_type: str, field: str) -> str:
    """Generate a title for the audio file."""
    return f"{word}_{word_type}_{field}_pronunciation"

def _extract_batch_data(anki_word: AnkiWordWithPronunciation) -> List[Dict[str, str]]:
    """Extract pronunciation data from AnkiWordWithPronunciation object into batch format."""
    word = anki_word.word
    word_type = anki_word.word_type
    
    # Get the pronunciation object for the word type using the _pronunciation suffix
    pronunciation_obj = getattr(anki_word, f"{word_type}_pronunciation", None)
    if not pronunciation_obj:
        return []
    
    batch_data = []
    fields = PRONUNCIATION_FIELDS.get(word_type, [])
    
    for field in fields:
        pronunciation_text = getattr(pronunciation_obj, field, None)
        if pronunciation_text:
            batch_data.append({
                'title': _generate_title(word, word_type, field),
                'pronunciation': pronunciation_text
            })
    
    return batch_data

async def _process_single_item(item: Dict[str, str]) -> Dict[str, str]:
    """Process a single pronunciation item, converting text to speech and saving as MP3."""
    title = item.get('title')
    pronunciation = item.get('pronunciation')
    
    if not title or not pronunciation:
        print(f"Skipping item with missing title or pronunciation: {item}")
        return item
    
    try:
        # Convert text to speech
        audio_data = await text_to_speech_narakeet(pronunciation)
        if audio_data is None:
            print(f"Failed to generate audio for pronunciation: {pronunciation}")
            return item
        
        # Save audio data
        filename = save_audio_data(audio_data, title)
        if filename is None:
            print(f"Failed to save audio file for title: {title}")
            return item
        
        # Return with Anki sound format
        return {
            'title': title,
            'pronunciation': f'[sound:{filename}]'
        }
        
    except Exception as e:
        print(f"Error processing item {title}: {e}")
        return item

def _handle_batch_results(results: List, batch_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Handle batch processing results, converting exceptions to original items."""
    processed_results = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Error in batch processing item {i}: {result}")
            processed_results.append(batch_data[i])
        else:
            processed_results.append(result)
    
    return processed_results

def _apply_results_to_word(anki_word: AnkiWordWithPronunciation, processed_results: List[Dict[str, str]]) -> AnkiWordWithPronunciation:
    """Apply processed results back to the AnkiWordWithPronunciation object."""
    title_to_pronunciation = {item['title']: item['pronunciation'] for item in processed_results}
    result = anki_word.model_copy()
    
    word_type = result.word_type
    pronunciation_obj = getattr(result, f"{word_type}_pronunciation", None)
    if not pronunciation_obj:
        return result
    
    # Update pronunciation fields with processed results
    fields = PRONUNCIATION_FIELDS.get(word_type, [])
    for field in fields:
        title_key = _generate_title(result.word, word_type, field)
        if title_key in title_to_pronunciation:
            setattr(pronunciation_obj, field, title_to_pronunciation[title_key])
    
    return result

async def process_word_pronunciation(anki_word: AnkiWordWithPronunciation) -> AnkiWordWithPronunciation:
    """
    Process an AnkiWordWithPronunciation object by converting all pronunciation text to speech and saving as MP3 files concurrently.
    
    Args:
        anki_word: AnkiWordWithPronunciation object with pronunciation text
        
    Returns:
        AnkiWordWithPronunciation object with pronunciation fields replaced by sound recordings in Anki format
    """
    # Extract batch data from the word pronunciation object
    batch_data = _extract_batch_data(anki_word)
    if not batch_data:
        return anki_word
    
    # Process all items concurrently
    tasks = [_process_single_item(item) for item in batch_data]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results and convert exceptions back to original items
    processed_results = _handle_batch_results(results, batch_data)
    
    # Apply results back to the AnkiWordWithPronunciation object
    return _apply_results_to_word(anki_word, processed_results)


def process_word_pronunciation_sync(anki_word: AnkiWordWithPronunciation) -> AnkiWordWithPronunciation:
    """
    Synchronous wrapper for process_word_pronunciation that can be used with AutoGen agents.
    
    Args:
        anki_word: AnkiWordWithPronunciation object with pronunciation text
        
    Returns:
        AnkiWordWithPronunciation object with pronunciation fields replaced by sound recordings in Anki format
    """
    return asyncio.run(process_word_pronunciation(anki_word)) 