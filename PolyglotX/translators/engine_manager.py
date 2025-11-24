from typing import Optional, Dict, Any, List
from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
import time


class TranslationEngine:
    def __init__(self, source: str = 'auto', target: str = 'ar'):
        self.source = source
        self.target = target
        
    def translate(self, text: str) -> str:
        raise NotImplementedError


class GoogleEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        translator = GoogleTranslator(source=self.source, target=self.target)
        return translator.translate(text)


class DeepLEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from deep_translator import DeepL
            translator = DeepL(source=self.source, target=self.target, use_free_api=True)
            return translator.translate(text)
        except:
            return GoogleEngine(self.source, self.target).translate(text)


class LibreEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        translator = LibreTranslator(source=self.source, target=self.target)
        return translator.translate(text)


class MyMemoryEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        translator = MyMemoryTranslator(source=self.source, target=self.target)
        return translator.translate(text)


class PonsEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from deep_translator import PonsTranslator
            translator = PonsTranslator(source=self.source, target=self.target)
            return translator.translate(text)
        except:
            return GoogleEngine(self.source, self.target).translate(text)


class LingueeEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from deep_translator import LingueeTranslator
            translator = LingueeTranslator(source=self.source, target=self.target)
            return translator.translate(text)
        except:
            return GoogleEngine(self.source, self.target).translate(text)


class YandexEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from deep_translator import YandexTranslator
            translator = YandexTranslator(source=self.source, target=self.target)
            return translator.translate(text)
        except:
            return GoogleEngine(self.source, self.target).translate(text)


class BingEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from deep_translator import MicrosoftTranslator
            translator = MicrosoftTranslator(source=self.source, target=self.target)
            return translator.translate(text)
        except:
            return GoogleEngine(self.source, self.target).translate(text)


class PapagoEngine(TranslationEngine):
    def translate(self, text: str) -> str:
        try:
            from translatepy import Translate
            t = Translate()
            result = t.translate(text, self.target)
            return result.result
        except:
            return GoogleEngine(self.source, self.target).translate(text)
