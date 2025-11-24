import re
import sys
import traceback
from typing import Dict, List, Any, Optional, Tuple
from PolyglotX.core.translator import Translator


class ErrorProcessor:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def process_exception(self, exc: Exception) -> Dict[str, Any]:
        return {
            'type': type(exc).__name__,
            'message': str(exc),
            'translated_type': self.translator.translate(type(exc).__name__),
            'translated_message': self.translator.translate(str(exc)),
            'traceback': self._extract_traceback(exc)
        }
    
    def _extract_traceback(self, exc: Exception) -> List[Dict[str, Any]]:
        tb_list = []
        tb = exc.__traceback__
        
        while tb is not None:
            frame = tb.tb_frame
            tb_list.append({
                'filename': frame.f_code.co_filename,
                'lineno': tb.tb_lineno,
                'function': frame.f_code.co_name,
                'code': self._get_code_context(frame.f_code.co_filename, tb.tb_lineno)
            })
            tb = tb.tb_next
        
        return tb_list
    
    def _get_code_context(self, filename: str, lineno: int, context: int = 3) -> List[str]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                start = max(0, lineno - context - 1)
                end = min(len(lines), lineno + context)
                return lines[start:end]
        except:
            return []
    
    def format_error_output(self, error_info: Dict[str, Any]) -> str:
        output = []
        output.append(f"{error_info['translated_type']}: {error_info['translated_message']}\n")
        
        for tb_entry in error_info['traceback']:
            output.append(f"  {self.translator.translate('File')} \"{tb_entry['filename']}\", {self.translator.translate('line')} {tb_entry['lineno']}, {self.translator.translate('in')} {tb_entry['function']}")
            
            if tb_entry['code']:
                for line in tb_entry['code']:
                    output.append(f"    {line.rstrip()}")
        
        return '\n'.join(output)


class StackTraceAnalyzer:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def analyze_stack(self, exc_traceback: Any) -> Dict[str, Any]:
        frames = []
        tb = exc_traceback
        
        while tb is not None:
            frame_info = {
                'file': tb.tb_frame.f_code.co_filename,
                'line': tb.tb_lineno,
                'function': tb.tb_frame.f_code.co_name,
                'locals': dict(tb.tb_frame.f_locals),
                'globals_count': len(tb.tb_frame.f_globals)
            }
            frames.append(frame_info)
            tb = tb.tb_next
        
        return {
            'depth': len(frames),
            'frames': frames,
            'top_frame': frames[0] if frames else None,
            'bottom_frame': frames[-1] if frames else None
        }
    
    def find_error_location(self, exc_traceback: Any) -> Tuple[str, int, str]:
        tb = exc_traceback
        while tb.tb_next is not None:
            tb = tb.tb_next
        
        frame = tb.tb_frame
        return frame.f_code.co_filename, tb.tb_lineno, frame.f_code.co_name


class ErrorClassifier:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def classify_error(self, exc: Exception) -> str:
        exc_type = type(exc).__name__
        
        categories = {
            'SyntaxError': 'syntax',
            'NameError': 'name',
            'TypeError': 'type',
            'ValueError': 'value',
            'AttributeError': 'attribute',
            'KeyError': 'key',
            'IndexError': 'index',
            'ImportError': 'import',
            'ModuleNotFoundError': 'import',
            'FileNotFoundError': 'file',
            'IOError': 'io',
            'OSError': 'os',
            'RuntimeError': 'runtime',
            'ZeroDivisionError': 'math',
            'OverflowError': 'math',
            'MemoryError': 'memory',
            'RecursionError': 'recursion'
        }
        
        return categories.get(exc_type, 'unknown')
    
    def get_severity(self, exc: Exception) -> str:
        critical_errors = ['MemoryError', 'SystemExit', 'KeyboardInterrupt']
        high_errors = ['SyntaxError', 'IndentationError', 'ImportError']
        medium_errors = ['TypeError', 'ValueError', 'AttributeError']
        
        exc_type = type(exc).__name__
        
        if exc_type in critical_errors:
            return 'critical'
        elif exc_type in high_errors:
            return 'high'
        elif exc_type in medium_errors:
            return 'medium'
        else:
            return 'low'


class ErrorEnricher:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def enrich_error(self, exc: Exception) -> Dict[str, Any]:
        enriched = {
            'original_type': type(exc).__name__,
            'original_message': str(exc),
            'translated_type': self.translator.translate(type(exc).__name__),
            'translated_message': self.translator.translate(str(exc)),
            'suggestions': self._get_suggestions(exc),
            'related_docs': self._get_related_docs(exc),
            'common_causes': self._get_common_causes(exc)
        }
        
        return enriched
    
    def _get_suggestions(self, exc: Exception) -> List[str]:
        exc_type = type(exc).__name__
        suggestions = {
            'NameError': [
                self.translator.translate('Check if the variable is defined'),
                self.translator.translate('Check for typos in variable name'),
                self.translator.translate('Ensure the variable is in scope')
            ],
            'TypeError': [
                self.translator.translate('Check argument types'),
                self.translator.translate('Ensure correct number of arguments'),
                self.translator.translate('Verify object supports the operation')
            ],
            'ValueError': [
                self.translator.translate('Check input value range'),
                self.translator.translate('Verify value format'),
                self.translator.translate('Ensure value is appropriate for operation')
            ],
            'FileNotFoundError': [
                self.translator.translate('Check if file exists'),
                self.translator.translate('Verify file path is correct'),
                self.translator.translate('Ensure you have read permissions')
            ]
        }
        
        return suggestions.get(exc_type, [])
    
    def _get_related_docs(self, exc: Exception) -> List[str]:
        exc_type = type(exc).__name__
        return [f"https://docs.python.org/3/library/exceptions.html#{exc_type}"]
    
    def _get_common_causes(self, exc: Exception) -> List[str]:
        exc_type = type(exc).__name__
        causes = {
            'NameError': [
                self.translator.translate('Variable not defined'),
                self.translator.translate('Misspelled variable name'),
                self.translator.translate('Variable out of scope')
            ],
            'ImportError': [
                self.translator.translate('Module not installed'),
                self.translator.translate('Wrong module name'),
                self.translator.translate('Circular import')
            ]
        }
        
        return causes.get(exc_type, [])
