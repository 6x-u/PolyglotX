import re
from typing import Optional, Dict, List
from translatepy import Translate


class LanguageDetector:
    def __init__(self):
        self._translator = Translate()
        self._language_patterns = self._init_patterns()
        
    def _init_patterns(self) -> Dict[str, List[str]]:
        return {
            'ar': [r'[\u0600-\u06FF]', r'[\u0750-\u077F]'],
            'tr': [r'[ğĞıİşŞ]'],
            'ja': [r'[\u3040-\u309F]', r'[\u30A0-\u30FF]', r'[\u4E00-\u9FAF]'],
            'zh': [r'[\u4E00-\u9FFF]'],
            'ku': [r'[\u0600-\u06FF]'],
            'es': [r'[ñáéíóúü]'],
            'hi': [r'[\u0900-\u097F]'],
            'fr': [r'[àâäæçéèêëîïôùûüÿœ]'],
            'ru': [r'[\u0400-\u04FF]'],
            'de': [r'[äöüßÄÖÜ]'],
            'pt': [r'[ãõçáéíóúâêôàü]']
        }
    
    def detect(self, text: str) -> Optional[str]:
        for lang, patterns in self._language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return lang
        
        try:
            result = self._translator.language(text)
            return result.alpha2 if hasattr(result, 'alpha2') else None
        except:
            return None
    
    def detect_with_confidence(self, text: str) -> Dict[str, float]:
        scores = {}
        
        for lang, patterns in self._language_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = len(re.findall(pattern, text))
                score += matches / len(text) if len(text) > 0 else 0.0
            scores[lang] = min(score, 1.0)
        
        return scores
    
    def is_language(self, text: str, language: str) -> bool:
        detected = self.detect(text)
        return detected == language


class ScriptDetector:
    def __init__(self):
        self._scripts = {
            'arabic': r'[\u0600-\u06FF]',
            'cyrillic': r'[\u0400-\u04FF]',
            'latin': r'[A-Za-z]',
            'chinese': r'[\u4E00-\u9FFF]',
            'japanese': r'[\u3040-\u309F\u30A0-\u30FF]',
            'korean': r'[\uAC00-\uD7AF]',
            'devanagari': r'[\u0900-\u097F]',
            'greek': r'[\u0370-\u03FF]',
            'hebrew': r'[\u0590-\u05FF]'
        }
    
    def detect_script(self, text: str) -> Optional[str]:
        for script, pattern in self._scripts.items():
            if re.search(pattern, text):
                return script
        return None
    
    def detect_all_scripts(self, text: str) -> List[str]:
        detected = []
        for script, pattern in self._scripts.items():
            if re.search(pattern, text):
                detected.append(script)
        return detected
