from typing import List, Callable, Optional, Any
from PolyglotX.translators.engine_manager import (
    GoogleEngine, LibreEngine, MyMemoryEngine
)


class FallbackHandler:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.engines = [
            GoogleEngine(target=language),
            MyMemoryEngine(target=language),
            LibreEngine(target=language)
        ]
        self._current_engine_index = 0
        
    def translate_with_fallback(self, text: str) -> str:
        for i, engine in enumerate(self.engines):
            try:
                result = engine.translate(text)
                if result and result != text:
                    self._current_engine_index = i
                    return result
            except Exception:
                continue
        
        return text
    
    def add_engine(self, engine: Any):
        self.engines.append(engine)
    
    def remove_engine(self, engine: Any):
        if engine in self.engines:
            self.engines.remove(engine)
    
    def get_current_engine(self) -> Optional[Any]:
        if 0 <= self._current_engine_index < len(self.engines):
            return self.engines[self._current_engine_index]
        return None


class ChainedFallback:
    def __init__(self, strategies: List[Callable]):
        self.strategies = strategies
        
    def execute(self, *args, **kwargs) -> Any:
        for strategy in self.strategies:
            try:
                result = strategy(*args, **kwargs)
                if result:
                    return result
            except:
                continue
        return None
