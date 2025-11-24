import sys
from typing import Optional, Any, Callable
from contextlib import contextmanager
from PolyglotX.core.exception_handler import ExceptionHandler


class ErrorContext:
    def __init__(self, language: str = 'ar', show_credits: bool = True):
        self.language = language
        self.show_credits = show_credits
        self.handler = ExceptionHandler(language=language, show_credits=show_credits)
        
    def __enter__(self):
        self.handler.install()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.handler._exception_hook(exc_type, exc_val, exc_tb)
            return True
        return False


@contextmanager
def translated_errors(language: str = 'ar', show_credits: bool = True):
    handler = ExceptionHandler(language=language, show_credits=show_credits)
    handler.install()
    try:
        yield handler
    finally:
        handler.uninstall()


@contextmanager
def suppress_translated_errors(language: str = 'ar'):
    handler = ExceptionHandler(language=language, show_credits=False, auto_exit=False)
    handler.install()
    try:
        yield
    except Exception:
        pass
    finally:
        handler.uninstall()


class ScopedExceptionHandler:
    def __init__(self, language: str = 'ar', callback: Optional[Callable] = None):
        self.language = language
        self.callback = callback
        self.handler = ExceptionHandler(language=language)
        
    def __enter__(self):
        self.handler.install()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.callback:
            self.callback(exc_type, exc_val, exc_tb)
        
        self.handler.uninstall()
        return False


class MultiLanguageContext:
    def __init__(self, primary_language: str = 'ar', fallback_language: str = 'en'):
        self.primary_language = primary_language
        self.fallback_language = fallback_language
        self.primary_handler = ExceptionHandler(language=primary_language)
        self.fallback_handler = ExceptionHandler(language=fallback_language)
        
    def __enter__(self):
        self.primary_handler.install()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            try:
                self.primary_handler._exception_hook(exc_type, exc_val, exc_tb)
            except:
                self.fallback_handler._exception_hook(exc_type, exc_val, exc_tb)
            return True
        return False
