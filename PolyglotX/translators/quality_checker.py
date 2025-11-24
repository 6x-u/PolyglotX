from typing import Dict, Any, List, Tuple
import re


class QualityChecker:
    def __init__(self):
        self.min_quality_score = 0.5
        
    def check_quality(self, original: str, translated: str) -> float:
        scores = []
        
        scores.append(self._check_length_ratio(original, translated))
        scores.append(self._check_special_characters(original, translated))
        scores.append(self._check_numbers_preserved(original, translated))
        scores.append(self._check_not_empty(translated))
        scores.append(self._check_not_identical(original, translated))
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _check_length_ratio(self, original: str, translated: str) -> float:
        if not original or not translated:
            return 0.0
        
        ratio = len(translated) / len(original)
        if 0.3 <= ratio <= 3.0:
            return 1.0
        elif ratio < 0.1 or ratio > 5.0:
            return 0.0
        else:
            return 0.5
    
    def _check_special_characters(self, original: str, translated: str) -> float:
        original_special = set(re.findall(r'[^\w\s]', original))
        translated_special = set(re.findall(r'[^\w\s]', translated))
        
        if not original_special:
            return 1.0
        
        preserved = len(original_special & translated_special) / len(original_special)
        return preserved
    
    def _check_numbers_preserved(self, original: str, translated: str) -> float:
        original_numbers = re.findall(r'\d+', original)
        translated_numbers = re.findall(r'\d+', translated)
        
        if not original_numbers:
            return 1.0
        
        if set(original_numbers) == set(translated_numbers):
            return 1.0
        else:
            return 0.5
    
    def _check_not_empty(self, translated: str) -> float:
        return 1.0 if translated and translated.strip() else 0.0
    
    def _check_not_identical(self, original: str, translated: str) -> float:
        if original == translated:
            return 0.5
        return 1.0
    
    def is_acceptable(self, original: str, translated: str) -> bool:
        score = self.check_quality(original, translated)
        return score >= self.min_quality_score
