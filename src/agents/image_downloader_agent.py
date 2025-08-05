from ..functions import save_image_from_url
from .config import create_agent

system_message = """
You are an image downloader agent that helps users download and save images.
Ask the user for an image url using the termination_msg field, then save the result.
"""

create_image_downloader_agent = create_agent(
    name="image_downloader_agent",
    system_message=system_message,
    default_functions=[save_image_from_url],
) 