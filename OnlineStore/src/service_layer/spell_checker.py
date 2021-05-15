from spellchecker import SpellChecker
from textblob import TextBlob
from autocorrect import Speller


class OurSpellChecker:
    def check_spelling(self, sentence: str):
        text_blb = TextBlob(sentence)
        text_corrected = text_blb.correct()
        return text_corrected
