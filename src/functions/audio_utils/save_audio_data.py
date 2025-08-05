import os
from typing import Optional

def save_audio_data(audio_data: bytes, filename: str, directory: str = None) -> Optional[str]:
    """
    Save audio data as MP3 file.
    
    Args:
        audio_data: The audio data as bytes
        filename: The filename to save the audio as (without .mp3 extension)
        directory: The directory to save the file in (defaults to ANKI_MEDIA_DIR environment variable)
        
    Returns:
        The filename if successful, None otherwise
    """
    try:
        # Use ANKI_MEDIA_DIR if directory is not provided
        if directory is None:
            directory = os.getenv('ANKI_MEDIA_DIR')

        # Ensure filename has .mp3 extension
        if not filename.endswith('.mp3'):
            filename = f"{filename}.mp3"
        
        # Expand tilde in path and resolve to absolute path
        expanded_directory = os.path.expanduser(directory)
        absolute_directory = os.path.abspath(expanded_directory)
        file_path = os.path.join(absolute_directory, filename)
        
        # Create directory if it doesn't exist
        os.makedirs(absolute_directory, exist_ok=True)
        
        # Save the audio data to file
        with open(file_path, 'wb') as f:
            f.write(audio_data)
        
        return filename
        
    except Exception as e:
        print(f"Error saving audio file: {e}")
        return None