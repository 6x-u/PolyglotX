import re
from typing import Any, List, Optional


def validate_language_code(code: str) -> bool:
    valid_codes = ['ar', 'tr', 'ja', 'zh', 'ku', 'es', 'hi', 'fr', 'ru', 'de', 'pt', 'en']
    return code.lower() in valid_codes


def validate_error_type(error_type: str) -> bool:
    common_types = [
        'Exception', 'TypeError', 'ValueError', 'NameError', 'AttributeError',
        'KeyError', 'IndexError', 'ImportError', 'IOError', 'OSError',
        'RuntimeError', 'SyntaxError', 'IndentationError', 'ZeroDivisionError'
    ]
    return error_type in common_types


def validate_translation(original: str, translated: str) -> bool:
    if not translated or not translated.strip():
        return False
    
    if translated == original:
        return False
    
    length_ratio = len(translated) / len(original) if len(original) > 0 else 0
    if length_ratio < 0.1 or length_ratio > 5.0:
        return False
    
    return True


def validate_config(config: dict) -> List[str]:
    errors = []
    
    required_keys = ['language', 'show_credits', 'auto_exit']
    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: {key}")
    
    if 'language' in config and not validate_language_code(config['language']):
        errors.append(f"Invalid language code: {config['language']}")
    
    return errors


def validate_exception(exc: Any) -> bool:
    return isinstance(exc, BaseException)


def validate_text_encoding(text: str) -> bool:
    try:
        text.encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False
