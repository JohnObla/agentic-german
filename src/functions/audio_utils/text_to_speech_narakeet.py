import os
from typing import Optional
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

def _get_request_body(text: str) -> str:
    """Generate the request body for Narakeet API."""
    return f"""---
voice: ulrich
narration-language: de-DE
---

{text}"""

def _get_headers(api_key: str) -> dict:
    """Generate headers for Narakeet API."""
    return {
        'Content-Type': 'text/plain',
        'accept': 'application/octet-stream',
        'x-api-key': api_key
    }

async def text_to_speech_narakeet(text: str) -> Optional[bytes]:
    """
    Convert text to speech using the Narakeet API.
    
    Args:
        text: The text to convert to speech
        
    Returns:
        The audio data as bytes if successful, None otherwise
    """
    if not AIOHTTP_AVAILABLE:
        raise ImportError("aiohttp library is required. Install with: pip install aiohttp")
    
    api_key = os.getenv('NARAKEET_API_KEY')
    if not api_key:
        raise ValueError("Narakeet API key is required. Set NARAKEET_API_KEY environment variable.")
    
    request_body = _get_request_body(text)
    headers = _get_headers(api_key)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.narakeet.com/text-to-speech/mp3',
                headers=headers,
                data=request_body,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                return await response.read()
        
    except aiohttp.ClientError as e:
        print(f"Error calling Narakeet API: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in text_to_speech_narakeet: {e}")
        return None 