import requests
from typing import Optional, Literal
from ..pdf_utils import pdf_to_markdown, transform_german_chars

def fetch_word_context(word: str, word_type: Literal["adverb", "noun", "adjective", "verb"]) -> Optional[str]:
    """
    Fetch word context from the appropriate URL based on word type and convert PDF to markdown.
    
    Args:
        word: The word to look up
        word_type: The type of word (adverb, noun, adjective, verb)
        
    Returns:
        The PDF content converted to markdown format, or None for adverbs or on error
    """
    # Return None for adverbs
    if word_type == "adverb":
        return """For the adverb field, use the example sentence in the example sentence field.
        Then use the anki cloze around the word in the example sentence cloze field.
        E.g.
        (regular) Komm raus! -> Komm raus!
        (cloze) Komm raus! -> Komm {{c1::raus}}!
        """
    
    # Transform German characters in the word for URL
    transformed_word = transform_german_chars(word, word_type)
    
    # Define URL patterns for each word type
    url_patterns = {
        "noun": f"https://www.verbformen.com/declension/nouns/{transformed_word}.pdf",
        "adjective": f"https://www.verbformen.com/declension/adjectives/{transformed_word}.pdf",
        "verb": f"https://www.verbformen.com/conjugation/{transformed_word}.pdf"
    }
    
    url = url_patterns.get(word_type)
    if not url:
        return None
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Convert PDF content to markdown
        pdf_content = response.content
        markdown_content = pdf_to_markdown(pdf_content)
        
        return markdown_content
    except requests.RequestException:
        print(f"Request failed for {url}")
        return None 