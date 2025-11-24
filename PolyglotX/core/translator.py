import sys
import threading
import time
from typing import Dict, List, Optional, Any, Callable, Tuple
from functools import lru_cache
from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator, PonsTranslator, LingueeTranslator
from translatepy import Translate
import re


class Translator:
    def __init__(self, target_language: str = 'ar', source_language: str = 'auto'):
        self.target_language = target_language
        self.source_language = source_language
        self._cache = {}
        self._lock = threading.Lock()
        self._engines = self._initialize_engines()
        self._translatepy = Translate()
        
    def _initialize_engines(self) -> List[Any]:
        engines = []
        try:
            engines.append(('google', GoogleTranslator))
        except:
            pass
        try:
            engines.append(('mymemory', MyMemoryTranslator))
        except:
            pass
        try:
            engines.append(('libre', LibreTranslator))
        except:
            pass
        try:
            engines.append(('pons', PonsTranslator))
        except:
            pass
        try:
            engines.append(('linguee', LingueeTranslator))
        except:
            pass
        return engines
    
    def translate(self, text: str, retry: int = 3) -> str:
        if not text or not text.strip():
            return text
            
        cache_key = f"{self.source_language}:{self.target_language}:{text}"
        
        with self._lock:
            if cache_key in self._cache:
                return self._cache[cache_key]
        
        for attempt in range(retry):
            for engine_name, engine_class in self._engines:
                try:
                    translator = engine_class(source=self.source_language, target=self.target_language)
                    result = translator.translate(text)
                    
                    with self._lock:
                        self._cache[cache_key] = result
                    
                    return result
                except Exception:
                    continue
            
            try:
                result = self._translatepy.translate(text, self.target_language).result
                with self._lock:
                    self._cache[cache_key] = result
                return result
            except:
                pass
            
            if attempt < retry - 1:
                time.sleep(0.5 * (attempt + 1))
        
        return text
    
    def translate_parts(self, text: str) -> str:
        parts = re.split(r'(["\'].*?["\']|`.*?`|\d+|[a-zA-Z_][a-zA-Z0-9_]*)', text)
        translated_parts = []
        
        for part in parts:
            if not part:
                continue
            if re.match(r'["\'].*?["\']|`.*?`|\d+|[a-zA-Z_][a-zA-Z0-9_]*', part):
                translated_parts.append(part)
            else:
                translated_parts.append(self.translate(part))
        
        return ''.join(translated_parts)
    
    def clear_cache(self):
        with self._lock:
            self._cache.clear()


class MultiEngineTranslator(Translator):
    def __init__(self, target_language: str = 'ar', engines: Optional[List[str]] = None):
        super().__init__(target_language)
        self.active_engines = engines or ['google', 'mymemory', 'libre']
        self._performance_metrics = {}
        
    def translate_with_consensus(self, text: str) -> str:
        results = []
        for engine_name, engine_class in self._engines:
            if engine_name in self.active_engines:
                try:
                    translator = engine_class(source=self.source_language, target=self.target_language)
                    result = translator.translate(text)
                    results.append(result)
                except:
                    continue
        
        if not results:
            return self.translate(text)
        
        from collections import Counter
        counter = Counter(results)
        return counter.most_common(1)[0][0]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        return self._performance_metrics


class CachedTranslator(Translator):
    def __init__(self, target_language: str = 'ar', cache_size: int = 10000):
        super().__init__(target_language)
        self.cache_size = cache_size
        self._access_count = {}
        self._cache_hits = 0
        self._cache_misses = 0
        
    @lru_cache(maxsize=10000)
    def _cached_translate(self, text: str) -> str:
        return super().translate(text)
    
    def translate(self, text: str, retry: int = 3) -> str:
        cache_key = f"{self.source_language}:{self.target_language}:{text}"
        
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]
        
        self._cache_misses += 1
        result = self._cached_translate(text)
        
        if len(self._cache) >= self.cache_size:
            self._evict_lru()
        
        self._cache[cache_key] = result
        return result
    
    def _evict_lru(self):
        if self._access_count:
            lru_key = min(self._access_count, key=self._access_count.get)
            del self._cache[lru_key]
            del self._access_count[lru_key]
    
    def get_cache_stats(self) -> Dict[str, int]:
        return {
            'hits': self._cache_hits,
            'misses': self._cache_misses,
            'size': len(self._cache),
            'hit_rate': self._cache_hits / (self._cache_hits + self._cache_misses) if (self._cache_hits + self._cache_misses) > 0 else 0
        }


class BatchTranslator(Translator):
    def __init__(self, target_language: str = 'ar', batch_size: int = 100):
        super().__init__(target_language)
        self.batch_size = batch_size
        self._pending_translations = []
        
    def add_to_batch(self, text: str) -> None:
        self._pending_translations.append(text)
    
    def translate_batch(self) -> List[str]:
        results = []
        for text in self._pending_translations:
            results.append(self.translate(text))
        self._pending_translations.clear()
        return results
    
    def auto_translate_batch(self, texts: List[str]) -> List[str]:
        batches = [texts[i:i+self.batch_size] for i in range(0, len(texts), self.batch_size)]
        all_results = []
        
        for batch in batches:
            batch_results = [self.translate(text) for text in batch]
            all_results.extend(batch_results)
        
        return all_results


class OfflineTranslator(Translator):
    def __init__(self, target_language: str = 'ar', dictionary_path: Optional[str] = None):
        super().__init__(target_language)
        self.dictionary_path = dictionary_path
        self._offline_dict = self._load_dictionary()
        
    def _load_dictionary(self) -> Dict[str, str]:
        offline_dict = {
            'error': {'ar': 'خطأ', 'tr': 'hata', 'es': 'error', 'fr': 'erreur', 'de': 'Fehler', 'ru': 'ошибка', 'ja': 'エラー', 'zh': '错误', 'hi': 'त्रुटि', 'pt': 'erro', 'ku': 'هەڵە'},
            'exception': {'ar': 'استثناء', 'tr': 'istisna', 'es': 'excepción', 'fr': 'exception', 'de': 'Ausnahme', 'ru': 'исключение', 'ja': '例外', 'zh': '异常', 'hi': 'अपवाद', 'pt': 'exceção', 'ku': 'ئەستەسنا'},
            'warning': {'ar': 'تحذير', 'tr': 'uyarı', 'es': 'advertencia', 'fr': 'avertissement', 'de': 'Warnung', 'ru': 'предупреждение', 'ja': '警告', 'zh': '警告', 'hi': 'चेतावनी', 'pt': 'aviso', 'ku': 'ئاگاداری'},
            'file': {'ar': 'ملف', 'tr': 'dosya', 'es': 'archivo', 'fr': 'fichier', 'de': 'Datei', 'ru': 'файл', 'ja': 'ファイル', 'zh': '文件', 'hi': 'फ़ाइल', 'pt': 'arquivo', 'ku': 'پەڕگە'},
            'line': {'ar': 'سطر', 'tr': 'satır', 'es': 'línea', 'fr': 'ligne', 'de': 'Zeile', 'ru': 'строка', 'ja': '行', 'zh': '行', 'hi': 'पंक्ति', 'pt': 'linha', 'ku': 'هێڵ'},
            'not found': {'ar': 'غير موجود', 'tr': 'bulunamadı', 'es': 'no encontrado', 'fr': 'non trouvé', 'de': 'nicht gefunden', 'ru': 'не найдено', 'ja': '見つかりません', 'zh': '未找到', 'hi': 'नहीं मिला', 'pt': 'não encontrado', 'ku': 'نەدۆزرایەوە'},
            'invalid': {'ar': 'غير صالح', 'tr': 'geçersiz', 'es': 'inválido', 'fr': 'invalide', 'de': 'ungültig', 'ru': 'недействительный', 'ja': '無効', 'zh': '无效', 'hi': 'अमान्य', 'pt': 'inválido', 'ku': 'نادروست'},
            'syntax error': {'ar': 'خطأ في بناء الجملة', 'tr': 'sözdizimi hatası', 'es': 'error de sintaxis', 'fr': 'erreur de syntaxe', 'de': 'Syntaxfehler', 'ru': 'синтаксическая ошибка', 'ja': '構文エラー', 'zh': '语法错误', 'hi': 'वाक्य-विन्यास त्रुटि', 'pt': 'erro de sintaxe', 'ku': 'هەڵەی ڕستەسازی'},
            'name error': {'ar': 'خطأ في الاسم', 'tr': 'isim hatası', 'es': 'error de nombre', 'fr': 'erreur de nom', 'de': 'Namensfehler', 'ru': 'ошибка имени', 'ja': '名前エラー', 'zh': '名称错误', 'hi': 'नाम त्रुटि', 'pt': 'erro de nome', 'ku': 'هەڵەی ناو'},
            'type error': {'ar': 'خطأ في النوع', 'tr': 'tip hatası', 'es': 'error de tipo', 'fr': 'erreur de type', 'de': 'Typfehler', 'ru': 'ошибка типа', 'ja': '型エラー', 'zh': '类型错误', 'hi': 'प्रकार त्रुटि', 'pt': 'erro de tipo', 'ku': 'هەڵەی جۆر'},
            'value error': {'ar': 'خطأ في القيمة', 'tr': 'değer hatası', 'es': 'error de valor', 'fr': 'erreur de valeur', 'de': 'Wertfehler', 'ru': 'ошибка значения', 'ja': '値エラー', 'zh': '值错误', 'hi': 'मान त्रुटि', 'pt': 'erro de valor', 'ku': 'هەڵەی بەها'},
        }
        
        return offline_dict
    
    def translate(self, text: str, retry: int = 3) -> str:
        text_lower = text.lower()
        for key, translations in self._offline_dict.items():
            if key in text_lower and self.target_language in translations:
                text = text.replace(key, translations[self.target_language])
        
        return super().translate(text, retry)


class AdaptiveTranslator(Translator):
    def __init__(self, target_language: str = 'ar'):
        super().__init__(target_language)
        self._quality_threshold = 0.7
        self._fallback_chain = ['google', 'mymemory', 'libre']
        
    def translate_with_quality_check(self, text: str) -> Tuple[str, float]:
        result = self.translate(text)
        quality_score = self._assess_quality(text, result)
        
        if quality_score < self._quality_threshold:
            for engine in self._fallback_chain:
                try:
                    result = self._translate_with_engine(text, engine)
                    quality_score = self._assess_quality(text, result)
                    if quality_score >= self._quality_threshold:
                        break
                except:
                    continue
        
        return result, quality_score
    
    def _translate_with_engine(self, text: str, engine: str) -> str:
        for engine_name, engine_class in self._engines:
            if engine_name == engine:
                translator = engine_class(source=self.source_language, target=self.target_language)
                return translator.translate(text)
        return text
    
    def _assess_quality(self, original: str, translated: str) -> float:
        if not translated or translated == original:
            return 0.0
        
        length_ratio = len(translated) / len(original) if len(original) > 0 else 0.0
        if length_ratio < 0.3 or length_ratio > 3.0:
            return 0.3
        
        return 0.8


class ContextAwareTranslator(Translator):
    def __init__(self, target_language: str = 'ar', context: Optional[Dict[str, Any]] = None):
        super().__init__(target_language)
        self.context = context or {}
        self._terminology = {}
        
    def set_context(self, context: Dict[str, Any]):
        self.context = context
    
    def add_terminology(self, term: str, translation: str):
        self._terminology[term.lower()] = translation
    
    def translate(self, text: str, retry: int = 3) -> str:
        for term, translation in self._terminology.items():
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            text = pattern.sub(translation, text)
        
        return super().translate(text, retry)


class TechnicalTranslator(Translator):
    def __init__(self, target_language: str = 'ar'):
        super().__init__(target_language)
        self._technical_terms = self._load_technical_terms()
        
    def _load_technical_terms(self) -> Dict[str, Dict[str, str]]:
        return {
            'function': {'ar': 'دالة', 'tr': 'fonksiyon', 'es': 'función', 'fr': 'fonction', 'de': 'Funktion', 'ru': 'функция', 'ja': '関数', 'zh': '函数', 'hi': 'फ़ंक्शन', 'pt': 'função', 'ku': 'فەنکشن'},
            'variable': {'ar': 'متغير', 'tr': 'değişken', 'es': 'variable', 'fr': 'variable', 'de': 'Variable', 'ru': 'переменная', 'ja': '変数', 'zh': '变量', 'hi': 'चर', 'pt': 'variável', 'ku': 'گۆڕاو'},
            'class': {'ar': 'فئة', 'tr': 'sınıf', 'es': 'clase', 'fr': 'classe', 'de': 'Klasse', 'ru': 'класс', 'ja': 'クラス', 'zh': '类', 'hi': 'वर्ग', 'pt': 'classe', 'ku': 'پۆل'},
            'module': {'ar': 'وحدة', 'tr': 'modül', 'es': 'módulo', 'fr': 'module', 'de': 'Modul', 'ru': 'модуль', 'ja': 'モジュール', 'zh': '模块', 'hi': 'मॉड्यूल', 'pt': 'módulo', 'ku': 'مۆدیول'},
            'import': {'ar': 'استيراد', 'tr': 'içe aktar', 'es': 'importar', 'fr': 'importer', 'de': 'importieren', 'ru': 'импорт', 'ja': 'インポート', 'zh': '导入', 'hi': 'आयात', 'pt': 'importar', 'ku': 'هاوردەکردن'},
            'object': {'ar': 'كائن', 'tr': 'nesne', 'es': 'objeto', 'fr': 'objet', 'de': 'Objekt', 'ru': 'объект', 'ja': 'オブジェクト', 'zh': '对象', 'hi': 'वस्तु', 'pt': 'objeto', 'ku': 'ئۆبجێکت'},
            'method': {'ar': 'طريقة', 'tr': 'yöntem', 'es': 'método', 'fr': 'méthode', 'de': 'Methode', 'ru': 'метод', 'ja': 'メソッド', 'zh': '方法', 'hi': 'विधि', 'pt': 'método', 'ku': 'میسۆد'},
            'attribute': {'ar': 'خاصية', 'tr': 'özellik', 'es': 'atributo', 'fr': 'attribut', 'de': 'Attribut', 'ru': 'атрибут', 'ja': '属性', 'zh': '属性', 'hi': 'गुण', 'pt': 'atributo', 'ku': 'تایبەتمەندی'},
        }
    
    def translate(self, text: str, retry: int = 3) -> str:
        for term, translations in self._technical_terms.items():
            if term in text.lower() and self.target_language in translations:
                pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                text = pattern.sub(translations[self.target_language], text)
        
        return super().translate(text, retry)


class SmartTranslator(Translator):
    def __init__(self, target_language: str = 'ar'):
        super().__init__(target_language)
        self._history = []
        self._preferences = {}
        
    def translate_smart(self, text: str) -> str:
        if self._should_preserve(text):
            return text
        
        result = self.translate(text)
        self._history.append((text, result))
        
        return result
    
    def _should_preserve(self, text: str) -> bool:
        if re.match(r'^[0-9]+$', text):
            return True
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', text):
            return True
        if text.startswith('"') and text.endswith('"'):
            return True
        if text.startswith("'") and text.endswith("'"):
            return True
        return False
    
    def learn_from_feedback(self, original: str, correct_translation: str):
        self._preferences[original] = correct_translation
    
    def translate(self, text: str, retry: int = 3) -> str:
        if text in self._preferences:
            return self._preferences[text]
        return super().translate(text, retry)
