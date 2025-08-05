# Agentic German Learning

An intelligent multi-agent system for German language learning that automatically creates Anki flashcards with comprehensive word information, pronunciation audio, and contextual images.

## Overview

Agentic German Learning is a sophisticated language learning tool that processes German words through a coordinated workflow of AI agents. Each agent specializes in a specific task - from determining word types to generating pronunciation audio - ultimately creating rich, multimedia Anki flashcards for effective German language learning.

## Features

### 🤖 Multi-Agent Architecture
- **7 specialized agents** working in a coordinated workflow
- **AG2 (AutoGen)** framework for agent orchestration
- **MLflow** integration for experiment tracking and monitoring

### 📚 Comprehensive Word Processing
- **Word type classification** (noun, verb, adjective, adverb)
- **Grammatical form generation** (conjugations, declensions, comparisons)
- **Context fetching** from authoritative German language sources
- **Example sentence creation** with cloze deletions for active recall

### 🔊 Audio Generation
- **Text-to-speech** using Narakeet API with German voice (Ulrich)
- **Pronunciation audio** for all word forms
- **Batch processing** for efficient audio generation

### 🖼️ Visual Learning
- **Automatic image downloading** for visual word association
- **Image integration** into Anki cards

### 📋 Anki Integration
- **Direct Anki card creation** using apy (Anki Python interface)
- **Multiple card templates**:
  - Deutsche Nomen (German Nouns)
  - Deutsche Verben (German Verbs) 
  - Deutsche Adjektive (German Adjectives)
  - Deutsche Vokabeln (German Vocabulary)

### 📊 Progress Tracking
- **Word list management** with 39K+ German words
- **Learning progress tracking** (already learned words)
- **CEFR level classification** (A1-C2)
- **Frequency-based ordering** for optimal learning sequence

## Architecture

The system uses a pipeline of 7 agents that process each word sequentially:

```
Get Item Agent → Word Type Agent → Word Context Agent → Image Downloader Agent → Word Pronunciation Agent → Dictation Agent → Anki Agent
```

### Agent Details

1. **Get Item Agent** (`human_input`)
   - Retrieves the next unlearned word from the German word list
   - Manages learning progress tracking

2. **Word Type Agent** (`automated`)
   - Classifies words into grammatical categories
   - Uses linguistic analysis and example sentences

3. **Word Context Agent** (`human_input`)
   - Fetches detailed grammatical information from verbformen.com
   - Generates conjugations, declensions, and comparative forms
   - Creates cloze deletion example sentences

4. **Image Downloader Agent** (`human_input`)
   - Downloads contextual images for visual learning
   - Integrates images into flashcard templates

5. **Word Pronunciation Agent** (`automated`)
   - Generates pronunciation data for all word forms
   - Prepares text for audio generation

6. **Dictation Agent** (`automated`)
   - Processes pronunciation data into audio files
   - Uses Narakeet TTS API for high-quality German audio

7. **Anki Agent** (`automated`)
   - Creates Anki cards using appropriate templates
   - Handles different word types with specialized fields

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [Anki](https://apps.ankiweb.net/) with [apy](https://github.com/lervag/apy) installed
- Narakeet API key for text-to-speech

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd agentic-german-learning
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   NARAKEET_API_KEY=your_narakeet_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_gemini_api_key_here  # If using Gemini models
   ```

4. **Set up Anki:**
   - Install and configure [apy](https://github.com/lervag/apy)
   - Ensure Anki is running and apy can connect to it
   - Import the required note types (Deutsche Nomen, Deutsche Verben, etc.)

## Usage

### Basic Usage

Run the main workflow to process a single word:

```bash
uv run main.py
```

This will:
1. Get the next unlearned German word
2. Process it through all agents
3. Create an Anki flashcard with audio and images
4. Mark the word as learned

### How main.py Works

The `main.py` file orchestrates the multi-agent workflow using a sophisticated **factory pattern** and **higher-order functions**:

#### 1. Agent Factory Pattern

Each `create_*_agent` function is a **factory function** that returns another function, not an agent instance:

```python
# This creates a factory function, NOT an agent instance
create_get_item_agent = create_agent(
    name="get_item_agent",
    system_message=system_message,
    default_functions=[get_current_word, get_next_word_from_current_word],
)
```

#### 2. Agent Instantiation with Executors

In `main.py`, agents are instantiated by calling factory functions with an **executor**:

```python
# This calls the factory function with an executor to create the actual agent
get_item_agent = create_get_item_agent(human_input)
word_context_agent = create_word_context_agent(human_input)
word_type_agent = create_word_type_agent(no_human_input)
```

Each factory function call returns a **dictionary object**:
```python
{
    "sender": executor,      # UserProxyAgent (human_input or no_human_input)
    "recipient": agent       # ConversableAgent with specific functionality
}
```

#### 3. Parameter Overrides

The factory pattern allows **parameter overrides** at instantiation time:

```python
# Using defaults
agent = create_get_item_agent(human_input)

# Overriding functions
agent = create_get_item_agent(
    human_input, 
    functions=[custom_function1, custom_function2]
)

# Overriding response format
agent = create_word_context_agent(
    human_input,
    response_format=CustomResponseSchema
)

# Overriding both
agent = create_anki_agent(
    no_human_input,
    functions=[add_word_to_anki, custom_anki_function],
    response_format=CustomAnkiResponse
)
```

#### 4. Workflow Execution

The `agent_workflow` list contains **dictionary objects** that define the sequential processing:

```python
agent_workflow = [
    get_item_agent,           # {"sender": human_input, "recipient": get_item_agent}
    word_type_agent,          # {"sender": no_human_input, "recipient": word_type_agent}
    word_context_agent,       # {"sender": human_input, "recipient": word_context_agent}
    image_downloader_agent,   # {"sender": human_input, "recipient": image_downloader_agent}
    word_pronunciation_agent, # {"sender": human_input, "recipient": word_pronunciation_agent}
    word_dictation_agent,     # {"sender": no_human_input, "recipient": dictation_agent}
    anki_agent               # {"sender": no_human_input, "recipient": anki_agent}
]
```

The `create_chat_configs()` function processes this workflow and creates configurations for AG2's `initiate_chats()` function, which executes each agent sequentially, passing the output of one agent as input to the next.

#### 5. Chat Configuration Overrides

The `create_chat_configs()` function also supports additional overrides for fine-tuning agent behavior:

```python
# Basic usage with default configuration
chat_configs = create_chat_configs(input_text, agent_workflow)

# Custom default configuration for all agents
custom_config = {
    "silent": True,                    # Suppress chat output for all agents
    "summary_method": "reflection_with_llm", # Summary method for all agents
    "max_turns": 3                     # Limit conversation turns for all agents
}
chat_configs = create_chat_configs(input_text, agent_workflow, custom_config)
```

**Per-Agent Overrides**: You can also modify individual agents in the workflow before passing to `create_chat_configs`:

```python
# Modify a specific agent's configuration
word_context_agent["message"] = "Please analyze this specific German word thoroughly"
word_context_agent["max_turns"] = 5
word_context_agent["silent"] = False

# Or add custom fields
image_downloader_agent["custom_prompt"] = "Focus on educational images"
anki_agent["card_type"] = "advanced"

agent_workflow = [
    get_item_agent,
    word_type_agent, 
    word_context_agent,     # Now has custom message and settings
    image_downloader_agent, # Now has custom prompt
    # ...
]
```

This flexibility allows you to:
- **Change input messages** to specific agents in the workflow
- **Adjust conversation parameters** (turns, silence, summary methods)
- **Add custom configuration** for specialized agent behavior
- **Override default settings** per agent or globally

### Configuration

#### Customize Agent Behavior

The system supports two execution modes:
- `human_input`: Requires user interaction and approval
- `no_human_input`: Fully automated execution

Modify `main.py` to adjust which agents require human input:

```python
# Human input agents (can be reviewed/modified)
get_item_agent = create_get_item_agent(human_input)
word_context_agent = create_word_context_agent(human_input)
image_downloader_agent = create_image_downloader_agent(human_input)

# Automated agents (no human interaction)
word_type_agent = create_word_type_agent(no_human_input)
word_dictation_agent = create_dictation_agent(no_human_input)
anki_agent = create_anki_agent(no_human_input)
```

#### Word List Management

The system uses two main data files:
- `src/data/german-word-list.json`: Complete word list (39K+ words)
- `src/data/already_learned_words.json`: Tracks learning progress

#### MLflow Tracking

Monitor your learning sessions through MLflow:

```bash
uv run mlflow ui
```

Visit `http://localhost:5000` to view experiment logs and metrics.

## Data Schema

### Word Structure

```python
class Word(BaseModel):
    word: str                        # The German word
    useful_for_flashcard: bool       # Learning priority flag
    cefr_level: str                  # A1, A2, B1, B2, C1, C2
    english_translation: str         # English meaning
    romanization: str                # Pronunciation guide
    example_sentence_native: str     # German example
    example_sentence_english: str    # English translation
    frequency_index: int             # Usage frequency ranking
```

### Anki Card Types

The system creates different card types based on word classification:

#### Nouns (Deutsche Nomen)
- Singular form with article (der/die/das)
- Plural form
- Pronunciation audio for both forms
- Visual image

#### Verbs (Deutsche Verben)  
- Infinitive, present, past, perfect forms
- Reflexive verb handling
- Pronunciation for all conjugations
- Visual image

#### Adjectives (Deutsche Adjektive)
- Positive, comparative, superlative forms
- Pronunciation audio
- Visual image

#### Adverbs (Deutsche Vokabeln)
- Example sentence with cloze deletion
- Pronunciation audio
- Visual image

## Testing

Run the test suite:

```bash
uv run pytest
```

Available test modules:
- `test_add_word_and_get_next.py`: Word processing workflow
- `test_get_current_word.py`: Word retrieval logic
- `test_get_next_unlearned_word.py`: Learning progress tracking
- `test_word_utils.py`: Utility function tests

## Project Structure

```
agentic-german-learning/
├── main.py                     # Main execution script
├── pyproject.toml             # Dependencies and configuration
├── src/
│   ├── agents/                # Agent implementations
│   │   ├── config/           # Agent configuration and factories
│   │   ├── anki_agent.py     # Anki card creation
│   │   ├── dictation_agent.py # Audio generation
│   │   ├── get_item_agent.py  # Word retrieval
│   │   ├── image_downloader_agent.py # Image processing
│   │   ├── word_context_agent.py     # Grammatical analysis
│   │   ├── word_pronunciation_agent.py # Pronunciation data
│   │   └── word_type_agent.py        # Word classification
│   ├── data/                 # Word lists and progress tracking
│   ├── functions/            # Core functionality modules
│   │   ├── anki_utils/      # Anki integration
│   │   ├── audio_utils/     # Text-to-speech processing
│   │   ├── image_utils/     # Image download and processing
│   │   ├── pdf_utils/       # PDF parsing for word context
│   │   └── word_management/ # Word list operations
│   └── schemas.py           # Data models and validation
├── tests/                   # Test suite
└── mlruns/                 # MLflow experiment tracking
```

## API Dependencies

### Required Services

1. **Narakeet API**: Text-to-speech generation
   - High-quality German voice synthesis
   - Sign up at [narakeet.com](https://www.narakeet.com/)

2. **OpenAI API**: LLM processing for most agents
   - GPT models for natural language understanding
   - Get API key from [platform.openai.com](https://platform.openai.com/)

3. **Google Gemini API** (optional): Alternative LLM provider
   - Can be used instead of or alongside OpenAI
   - Get API key from [Google AI Studio](https://aistudio.google.com/)

### External Data Sources

- **verbformen.com**: Authoritative German grammatical data
  - Automatic PDF fetching and parsing
  - Verb conjugations and noun declensions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

[Add your license information here]

## Support

For questions, issues, or contributions, please [open an issue](link-to-issues) or contact the maintainers.

---

**Happy German Learning! 🇩🇪📚**
