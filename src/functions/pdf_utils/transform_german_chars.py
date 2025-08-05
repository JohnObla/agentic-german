from typing import Literal

def transform_german_chars(text: str, word_type: Literal["verb", "noun", "adjective", "adverb"]) -> str:
    """
    Transform German umlauts and eszett in a string.
    
    Args:
        text: The input string to transform
        
    Returns:
        The transformed string with umlauts and eszett replaced
    """
    char_mapping = {
        'ä': 'a3',
        'ö': 'o3', 
        'ü': 'u3',
        'ß': 's5'
    }
    
    for char, replacement in char_mapping.items():
        text = text.replace(char, replacement)
    
    if word_type == "noun":
        text = text.capitalize()
    
    return text 