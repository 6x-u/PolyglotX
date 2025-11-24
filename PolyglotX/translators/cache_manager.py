import json
import os
import pickle
import threading
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class CacheManager:
    def __init__(self, cache_file: str = '.polyglotx_cache.json'):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.lock = threading.Lock()
        
    def _load_cache(self) -> Dict[str, Any]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str) -> Optional[str]:
        with self.lock:
            return self.cache.get(key)
    
    def set(self, key: str, value: str):
        with self.lock:
            self.cache[key] = value
            self._save_cache()
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self._save_cache()
    
    def size(self) -> int:
        with self.lock:
            return len(self.cache)


class TTLCache(CacheManager):
    def __init__(self, cache_file: str = '.polyglotx_ttl_cache.json', ttl: int = 3600):
        super().__init__(cache_file)
        self.ttl = ttl
        
    def get(self, key: str) -> Optional[str]:
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                if isinstance(entry, dict) and 'value' in entry and 'timestamp' in entry:
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                        return entry['value']
                    else:
                        del self.cache[key]
            return None
    
    def set(self, key: str, value: str):
        with self.lock:
            self.cache[key] = {
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            self._save_cache()
