import json
from typing import List, Dict, Any
from PolyglotX.core.translator import BatchTranslator


class BatchProcessor:
    def __init__(self, language: str = 'ar', batch_size: int = 100):
        self.language = language
        self.translator = BatchTranslator(target_language=language, batch_size=batch_size)
        
    def process_file(self, input_file: str, output_file: str):
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated = self.translator.auto_translate_batch(lines)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(translated)
    
    def process_json(self, input_file: str, output_file: str):
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            translated = self.translator.auto_translate_batch(data)
        elif isinstance(data, dict):
            translated = {}
            for key, value in data.items():
                if isinstance(value, str):
                    translated[key] = self.translator.translate(value)
                else:
                    translated[key] = value
        else:
            translated = data
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated, f, ensure_ascii=False, indent=2)
