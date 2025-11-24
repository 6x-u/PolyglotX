import sys
import threading
from typing import Callable, List, Dict, Any, Optional


class HookManager:
    def __init__(self):
        self._pre_hooks = []
        self._post_hooks = []
        self._error_hooks = []
        self._lock = threading.Lock()
        
    def add_pre_hook(self, hook: Callable):
        with self._lock:
            self._pre_hooks.append(hook)
    
    def add_post_hook(self, hook: Callable):
        with self._lock:
            self._post_hooks.append(hook)
    
    def add_error_hook(self, hook: Callable):
        with self._lock:
            self._error_hooks.append(hook)
    
    def remove_pre_hook(self, hook: Callable):
        with self._lock:
            if hook in self._pre_hooks:
                self._pre_hooks.remove(hook)
    
    def remove_post_hook(self, hook: Callable):
        with self._lock:
            if hook in self._post_hooks:
                self._post_hooks.remove(hook)
    
    def remove_error_hook(self, hook: Callable):
        with self._lock:
            if hook in self._error_hooks:
                self._error_hooks.remove(hook)
    
    def execute_pre_hooks(self, *args, **kwargs):
        with self._lock:
            for hook in self._pre_hooks:
                try:
                    hook(*args, **kwargs)
                except:
                    pass
    
    def execute_post_hooks(self, *args, **kwargs):
        with self._lock:
            for hook in self._post_hooks:
                try:
                    hook(*args, **kwargs)
                except:
                    pass
    
    def execute_error_hooks(self, *args, **kwargs):
        with self._lock:
            for hook in self._error_hooks:
                try:
                    hook(*args, **kwargs)
                except:
                    pass
    
    def clear_all_hooks(self):
        with self._lock:
            self._pre_hooks.clear()
            self._post_hooks.clear()
            self._error_hooks.clear()


class ExceptionHookManager:
    def __init__(self):
        self._original_excepthook = sys.excepthook
        self._hooks = []
        self._lock = threading.Lock()
        
    def add_hook(self, hook: Callable):
        with self._lock:
            self._hooks.append(hook)
        self._install()
    
    def remove_hook(self, hook: Callable):
        with self._lock:
            if hook in self._hooks:
                self._hooks.remove(hook)
    
    def _install(self):
        sys.excepthook = self._exception_hook
    
    def _exception_hook(self, exc_type, exc_value, exc_traceback):
        with self._lock:
            for hook in self._hooks:
                try:
                    hook(exc_type, exc_value, exc_traceback)
                except:
                    pass
        
        self._original_excepthook(exc_type, exc_value, exc_traceback)
    
    def restore(self):
        sys.excepthook = self._original_excepthook
