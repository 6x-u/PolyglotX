import re
import hashlib
import traceback
from typing import Dict, Any, List, Optional, Tuple
from PolyglotX.core.language_detector import LanguageDetector


def detect_language(text: str) -> Optional[str]:
    detector = LanguageDetector()
    return detector.detect(text)


def extract_error_info(exc: Exception) -> Dict[str, Any]:
    return {
        'type': type(exc).__name__,
        'message': str(exc),
        'args': exc.args,
        'traceback': traceback.format_tb(exc.__traceback__) if exc.__traceback__ else []
    }


def format_stack_trace(tb: Any) -> List[str]:
    return traceback.format_tb(tb)


def parse_exception(exc_info: tuple) -> Dict[str, Any]:
    exc_type, exc_value, exc_traceback = exc_info
    return {
        'type': exc_type.__name__ if exc_type else 'Unknown',
        'value': str(exc_value) if exc_value else '',
        'traceback': format_stack_trace(exc_traceback) if exc_traceback else []
    }


def sanitize_error_message(message: str) -> str:
    message = re.sub(r'File "([^"]+)"', r'File "\1"', message)
    message = re.sub(r'\n+', '\n', message)
    return message.strip()


def get_error_context(exc: Exception, lines_before: int = 3, lines_after: int = 3) -> Dict[str, Any]:
    tb = exc.__traceback__
    if not tb:
        return {}
    
    frame = tb.tb_frame
    lineno = tb.tb_lineno
    filename = frame.f_code.co_filename
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            start = max(0, lineno - lines_before - 1)
            end = min(len(all_lines), lineno + lines_after)
            context_lines = all_lines[start:end]
            
            return {
                'filename': filename,
                'lineno': lineno,
                'context': context_lines,
                'error_line': all_lines[lineno - 1] if 0 <= lineno - 1 < len(all_lines) else ''
            }
    except:
        return {}


def calculate_error_hash(exc: Exception) -> str:
    error_str = f"{type(exc).__name__}:{str(exc)}"
    return hashlib.md5(error_str.encode()).hexdigest()


def group_similar_errors(errors: List[Exception]) -> Dict[str, List[Exception]]:
    groups = {}
    for error in errors:
        error_hash = calculate_error_hash(error)
        if error_hash not in groups:
            groups[error_hash] = []
        groups[error_hash].append(error)
    return groups


def suggest_fixes(exc: Exception) -> List[str]:
    exc_type = type(exc).__name__
    
    suggestions = {
        'NameError': [
            'Check if the variable is defined before use',
            'Verify the spelling of the variable name',
            'Ensure the variable is in the correct scope'
        ],
        'TypeError': [
            'Check the types of arguments passed to the function',
            'Verify the number of arguments matches the function signature',
            'Ensure the object supports the operation'
        ],
        'ValueError': [
            'Check if the value is in the expected range',
            'Verify the format of the input value',
            'Ensure the value is appropriate for the operation'
        ],
        'ImportError': [
            'Check if the module is installed',
            'Verify the module name is correct',
            'Ensure the module is in PYTHONPATH'
        ],
        'FileNotFoundError': [
            'Verify the file path is correct',
            'Check if the file exists',
            'Ensure you have read permissions'
        ]
    }
    
    return suggestions.get(exc_type, ['No specific suggestions available'])


def find_error_documentation(exc: Exception) -> str:
    exc_type = type(exc).__name__
    return f"https://docs.python.org/3/library/exceptions.html#{exc_type}"
