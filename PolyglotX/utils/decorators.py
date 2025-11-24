import functools
import time
import logging
from typing import Callable, Any, Optional, Type
from PolyglotX.core.exception_handler import ExceptionHandler


def handle_exceptions(language: str = 'ar', show_credits: bool = True):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            handler = ExceptionHandler(language=language, show_credits=show_credits)
            handler.install()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler._exception_hook(type(e), e, e.__traceback__)
            finally:
                handler.uninstall()
        return wrapper
    return decorator


def translate_errors(language: str = 'ar'):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            handler = ExceptionHandler(language=language)
            handler.install()
            try:
                return func(*args, **kwargs)
            finally:
                handler.uninstall()
        return wrapper
    return decorator


def retry_on_error(max_retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator


def fallback_on_error(fallback_value: Any = None):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return fallback_value
        return wrapper
    return decorator


def log_exceptions(logger: Optional[logging.Logger] = None):
    if logger is None:
        logger = logging.getLogger(__name__)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


def measure_exception_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"Exception occurred after {elapsed:.2f} seconds")
            raise
    return wrapper


def suppress_exceptions(*exception_types):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types:
                pass
        return wrapper
    return decorator


def transform_exception(from_exc: Type[Exception], to_exc: Type[Exception]):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except from_exc as e:
                raise to_exc(str(e)) from e
        return wrapper
    return decorator


def validate_exception(condition: Callable[[Exception], bool]):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if condition(e):
                    raise
                else:
                    pass
        return wrapper
    return decorator


def notify_on_exception(callback: Callable):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                callback(e)
                raise
        return wrapper
    return decorator
