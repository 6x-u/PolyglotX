import sys
import traceback
import threading
import inspect
import os
from typing import Optional, Callable, Any, Dict, List, Type
from datetime import datetime
from PolyglotX.core.translator import Translator, SmartTranslator


class ExceptionHandler:
    def __init__(self, language: str = 'ar', show_credits: bool = True, auto_exit: bool = True):
        self.language = language
        self.show_credits = show_credits
        self.auto_exit = auto_exit
        self.translator = SmartTranslator(target_language=language)
        self._original_excepthook = sys.excepthook
        self._installed = False
        self._error_count = 0
        self._error_history = []
        
    def install(self):
        if not self._installed:
            sys.excepthook = self._exception_hook
            self._installed = True
    
    def uninstall(self):
        if self._installed:
            sys.excepthook = self._original_excepthook
            self._installed = False
    
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        self._error_count += 1
        self._error_history.append({
            'type': exc_type.__name__,
            'message': str(exc_value),
            'time': datetime.now().isoformat()
        })
        
        error_type = exc_type.__name__
        error_message = str(exc_value)
        
        translated_type = self.translator.translate(error_type)
        translated_message = self.translator.translate(error_message)
        
        print(f"\n{translated_type}: {translated_message}\n")
        
        if exc_traceback:
            tb_lines = traceback.format_tb(exc_traceback)
            for line in tb_lines:
                translated_line = self._translate_traceback_line(line)
                print(translated_line, end='')
        
        if self.show_credits:
            credits_message = self._get_credits_message()
            print(f"\n{credits_message}")
        
        if self.auto_exit:
            sys.exit(1)
    
    def _translate_traceback_line(self, line: str) -> str:
        parts = line.split(',')
        translated_parts = []
        
        for part in parts:
            if 'File' in part or 'line' in part:
                translated_part = self.translator.translate_parts(part)
                translated_parts.append(translated_part)
            else:
                translated_parts.append(part)
        
        return ','.join(translated_parts)
    
    def _get_credits_message(self) -> str:
        messages = {
            'ar': 'MERO tele QP4RM',
            'tr': 'MERO tele QP4RM',
            'es': 'MERO tele QP4RM',
            'fr': 'MERO tele QP4RM',
            'de': 'MERO tele QP4RM',
            'ru': 'MERO tele QP4RM',
            'ja': 'MERO tele QP4RM',
            'zh': 'MERO tele QP4RM',
            'hi': 'MERO tele QP4RM',
            'pt': 'MERO tele QP4RM',
            'ku': 'MERO tele QP4RM',
        }
        return messages.get(self.language, 'MERO tele QP4RM')
    
    def get_error_stats(self) -> Dict[str, Any]:
        return {
            'total_errors': self._error_count,
            'history': self._error_history
        }


class GlobalExceptionHandler(ExceptionHandler):
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, language: str = 'ar', **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, language: str = 'ar', show_credits: bool = True, auto_exit: bool = True):
        if not hasattr(self, '_initialized'):
            super().__init__(language, show_credits, auto_exit)
            self._initialized = True


class ErrorTranslator:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def translate_error(self, error: Exception) -> str:
        error_type = type(error).__name__
        error_message = str(error)
        
        translated_type = self.translator.translate(error_type)
        translated_message = self.translator.translate(error_message)
        
        return f"{translated_type}: {translated_message}"
    
    def translate_traceback(self, tb: Any) -> List[str]:
        tb_lines = traceback.format_tb(tb)
        translated_lines = []
        
        for line in tb_lines:
            translated_line = self.translator.translate_parts(line)
            translated_lines.append(translated_line)
        
        return translated_lines


class TracebackTranslator:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        
    def format_traceback(self, exc_info: tuple) -> str:
        exc_type, exc_value, exc_traceback = exc_info
        
        lines = []
        lines.append(self.translator.translate("Traceback (most recent call last):"))
        
        tb_lines = traceback.format_tb(exc_traceback)
        for line in tb_lines:
            translated_line = self.translator.translate_parts(line)
            lines.append(translated_line)
        
        error_line = f"{exc_type.__name__}: {exc_value}"
        translated_error = self.translator.translate(error_line)
        lines.append(translated_error)
        
        return '\n'.join(lines)


class ContextualErrorHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar', include_locals: bool = True, include_globals: bool = False):
        super().__init__(language)
        self.include_locals = include_locals
        self.include_globals = include_globals
        
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        super()._exception_hook(exc_type, exc_value, exc_traceback)
        
        if self.include_locals or self.include_globals:
            frame = exc_traceback.tb_frame
            
            if self.include_locals:
                print(f"\n{self.translator.translate('Local variables')}:")
                for key, value in frame.f_locals.items():
                    print(f"  {key} = {repr(value)}")
            
            if self.include_globals:
                print(f"\n{self.translator.translate('Global variables')}:")
                for key, value in frame.f_globals.items():
                    if not key.startswith('__'):
                        print(f"  {key} = {repr(value)}")


class AsyncExceptionHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar'):
        super().__init__(language)
        self._async_errors = []
        
    async def handle_async_exception(self, coro):
        try:
            return await coro
        except Exception as e:
            self._async_errors.append(e)
            error_msg = self.translator.translate_error(e)
            print(f"\n{error_msg}")
            if self.show_credits:
                print(f"\n{self._get_credits_message()}")
            raise
    
    def get_async_errors(self) -> List[Exception]:
        return self._async_errors


class ThreadSafeExceptionHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar'):
        super().__init__(language)
        self._thread_lock = threading.Lock()
        self._thread_errors = {}
        
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        thread_id = threading.get_ident()
        
        with self._thread_lock:
            if thread_id not in self._thread_errors:
                self._thread_errors[thread_id] = []
            
            self._thread_errors[thread_id].append({
                'type': exc_type.__name__,
                'message': str(exc_value),
                'time': datetime.now().isoformat()
            })
        
        super()._exception_hook(exc_type, exc_value, exc_traceback)
    
    def get_thread_errors(self, thread_id: Optional[int] = None) -> Dict[int, List[Dict]]:
        if thread_id:
            return {thread_id: self._thread_errors.get(thread_id, [])}
        return self._thread_errors


class ChainedExceptionHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar', handlers: Optional[List[Callable]] = None):
        super().__init__(language)
        self.handlers = handlers or []
        
    def add_handler(self, handler: Callable):
        self.handlers.append(handler)
    
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        for handler in self.handlers:
            try:
                handler(exc_type, exc_value, exc_traceback)
            except:
                pass
        
        super()._exception_hook(exc_type, exc_value, exc_traceback)


class FilteredExceptionHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar', exception_types: Optional[List[Type[Exception]]] = None):
        super().__init__(language)
        self.exception_types = exception_types or [Exception]
        
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        if any(issubclass(exc_type, et) for et in self.exception_types):
            super()._exception_hook(exc_type, exc_value, exc_traceback)
        else:
            self._original_excepthook(exc_type, exc_value, exc_traceback)


class LoggingExceptionHandler(ExceptionHandler):
    def __init__(self, language: str = 'ar', log_file: Optional[str] = None):
        super().__init__(language)
        self.log_file = log_file or 'polyglotx_errors.log'
        
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Type: {exc_type.__name__}\n")
            f.write(f"Message: {exc_value}\n")
            f.write(f"Traceback:\n")
            traceback.print_tb(exc_traceback, file=f)
            f.write(f"\n{'='*80}\n")
        
        super()._exception_hook(exc_type, exc_value, exc_traceback)
