import signal
import sys
from typing import Callable, Optional, Dict, Any
from PolyglotX.core.translator import Translator


class SignalHandler:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        self._handlers = {}
        
    def register(self, sig: int, handler: Callable):
        self._handlers[sig] = handler
        signal.signal(sig, handler)
    
    def unregister(self, sig: int):
        if sig in self._handlers:
            signal.signal(sig, signal.SIG_DFL)
            del self._handlers[sig]
    
    def handle_sigint(self, sig, frame):
        message = self.translator.translate("Program interrupted by user")
        print(f"\n{message}")
        sys.exit(0)
    
    def handle_sigterm(self, sig, frame):
        message = self.translator.translate("Program terminated")
        print(f"\n{message}")
        sys.exit(0)
    
    def setup_default_handlers(self):
        self.register(signal.SIGINT, self.handle_sigint)
        self.register(signal.SIGTERM, self.handle_sigterm)


class InterruptHandler:
    def __init__(self, language: str = 'ar', callback: Optional[Callable] = None):
        self.language = language
        self.callback = callback
        self.translator = Translator(target_language=language)
        self._original_handler = None
        
    def __enter__(self):
        self._original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._handle_interrupt)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.signal(signal.SIGINT, self._original_handler)
    
    def _handle_interrupt(self, sig, frame):
        if self.callback:
            self.callback(sig, frame)
        
        message = self.translator.translate("Interrupted")
        print(f"\n{message}")
        sys.exit(0)
