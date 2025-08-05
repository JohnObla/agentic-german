from typing import Literal, Optional
from pydantic import BaseModel, Field

class BaseWord(BaseModel):
    word_type: Literal["verb", "noun", "adjective", "adverb"]
    word: str

class Noun(BaseModel):
    singular: str
    plural: str | None = None

class Verb(BaseModel):
    infinitive: str
    present: str
    written_past: str
    spoken_past: str

class Adjective(BaseModel):
    positive: str
    comparative: str | None = None
    superlative: str | None = None

class AdverbForPronunciation(BaseModel):
    example_sentence: str

class Adverb(AdverbForPronunciation):
    adverb: str
    cloze_example_sentence: str

# -- MAIN RESPONSE TYPES --
class AddTerminationMsg(BaseModel):
    termination_msg: str

class Word(BaseModel):
    word: str
    useful_for_flashcard: bool
    cefr_level: str
    english_translation: str
    romanization: str
    example_sentence_native: str
    example_sentence_english: str
    frequency_index: int

class AnkiWord(BaseWord):
    image_filename: Optional[str] = None
    noun: Optional[Noun] = None
    verb: Optional[Verb] = None
    adjective: Optional[Adjective] = None
    adverb: Optional[Adverb] = None

class AnkiWordWithPronunciation(AnkiWord):
    noun_pronunciation: Optional[Noun] = None
    verb_pronunciation: Optional[Verb] = None
    adjective_pronunciation: Optional[Adjective] = None
    adverb_pronunciation: Optional[AdverbForPronunciation] = None

class AnkiResponse(BaseModel):
    anki_output: str 