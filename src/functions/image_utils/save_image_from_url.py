import os
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from src.schemas import BaseWord

def save_image_from_url(image_url: str, word_type_obj: BaseWord, directory: str | None = None) -> str:
    """
    Download an image from a URL, resize it to 400px width while maintaining aspect ratio,
    and save it to the specified file location with a formatted filename.
    
    Args:
        image_url: The URL of the image to download
        word_type_obj: The WordType object containing word and word_type information
        directory: The directory to save the file in (defaults to ANKI_MEDIA_DIR environment variable)
        
    Returns:
        The formatted filename if the image was successfully downloaded, resized, and saved
        
    Raises:
        ValueError: If no valid filename can be extracted from the URL or if ANKI_MEDIA_DIR is not set
    """
    try:
        # Extract filename from URL path
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename or '.' not in filename:
            raise ValueError(f"Could not extract a valid filename from URL path: {image_url}")
        
        # Extract file extension
        _, file_extension = os.path.splitext(filename)
        
        # Generate formatted filename
        formatted_filename = f"agentic-{word_type_obj.word}-{word_type_obj.word_type}{file_extension}"
        
        # Construct full file path
        if directory is None:
            directory = os.getenv('ANKI_MEDIA_DIR')
            if directory is None:
                raise ValueError("ANKI_MEDIA_DIR environment variable is not set. Please set it or provide a directory parameter.")
        
        # Expand tilde in path and resolve to absolute path
        expanded_directory = os.path.expanduser(directory)
        absolute_directory = os.path.abspath(expanded_directory)
        file_path = os.path.join(absolute_directory, formatted_filename)
        
        # Create directory if it doesn't exist
        os.makedirs(absolute_directory, exist_ok=True)
        
        # Download the image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Open the image using Pillow
        image = Image.open(BytesIO(response.content))
        
        # Calculate new height to maintain aspect ratio with 400px width
        target_width = 400
        aspect_ratio = image.width / image.height
        target_height = int(target_width / aspect_ratio)
        
        # Resize the image
        resized_image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Save the resized image
        resized_image.save(file_path)
        
        return formatted_filename
        
    except requests.RequestException as e:
        print(f"Error downloading image from {image_url}: {e}")
        raise
    except IOError as e:
        print(f"Error saving image to {file_path}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise