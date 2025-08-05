import mlflow
from dotenv import load_dotenv
from src.agents.anki_agent import create_anki_agent
from src.agents.get_item_agent import create_get_item_agent
from src.agents.image_downloader_agent import create_image_downloader_agent
from src.agents.dictation_agent import create_dictation_agent
from src.agents.word_type_agent import create_word_type_agent
from src.agents.word_context_agent import create_word_context_agent
from src.agents.word_pronunciation_agent import create_word_pronunciation_agent
from src.agents.config import human_input, no_human_input, create_chat_configs
from autogen import initiate_chats

# Load environment variables from .env file
load_dotenv()

mlflow.ag2.autolog()
mlflow.set_experiment("AG2")

input_text = "Get current word."

# human input
get_item_agent = create_get_item_agent(human_input)
word_context_agent = create_word_context_agent(human_input)
image_downloader_agent = create_image_downloader_agent(human_input)
word_pronunciation_agent = create_word_pronunciation_agent(human_input)

# automated input
word_type_agent = create_word_type_agent(no_human_input)
word_dictation_agent = create_dictation_agent(no_human_input)
anki_agent = create_anki_agent(no_human_input)

agent_workflow = [
    get_item_agent,
    word_type_agent,
    word_context_agent,
    image_downloader_agent,
    word_pronunciation_agent,
    word_dictation_agent,
    anki_agent
]

chat_configs = create_chat_configs(input_text, agent_workflow)
chat_results = initiate_chats(chat_configs)
