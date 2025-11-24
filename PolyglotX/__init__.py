__version__ = "1.0.0"
__author__ = "MERO"
__contact__ = "@QP4RM"
__description__ = "Advanced multilingual exception handler and translator for Python applications"
__license__ = "MIT"

from PolyglotX.languages.arbe import arbe
from PolyglotX.languages.tr import tr
from PolyglotX.languages.ja import ja
from PolyglotX.languages.zh import zh
from PolyglotX.languages.ku import ku
from PolyglotX.languages.es import es
from PolyglotX.languages.hi import hi
from PolyglotX.languages.fr import fr
from PolyglotX.languages.ru import ru
from PolyglotX.languages.de import de
from PolyglotX.languages.pt import pt

from PolyglotX.core.exception_handler import (
    ExceptionHandler,
    GlobalExceptionHandler,
    ErrorTranslator,
    TracebackTranslator,
    ContextualErrorHandler,
    AsyncExceptionHandler,
    ThreadSafeExceptionHandler,
    ChainedExceptionHandler,
    FilteredExceptionHandler,
    LoggingExceptionHandler
)

from PolyglotX.core.translator import (
    Translator,
    MultiEngineTranslator,
    CachedTranslator,
    BatchTranslator,
    OfflineTranslator,
    AdaptiveTranslator,
    ContextAwareTranslator,
    TechnicalTranslator,
    SmartTranslator
)

from PolyglotX.handlers.error_formatter import (
    ErrorFormatter,
    ColoredErrorFormatter,
    HTMLErrorFormatter,
    JSONErrorFormatter,
    XMLErrorFormatter,
    MarkdownErrorFormatter,
    PlainTextErrorFormatter,
    RichErrorFormatter,
    CompactErrorFormatter,
    VerboseErrorFormatter
)

from PolyglotX.handlers.output_handler import (
    OutputHandler,
    ConsoleOutputHandler,
    FileOutputHandler,
    SyslogOutputHandler,
    EmailOutputHandler,
    WebhookOutputHandler,
    DatabaseOutputHandler,
    StreamOutputHandler,
    BufferedOutputHandler,
    AsyncOutputHandler
)

from PolyglotX.utils.helpers import (
    detect_language,
    extract_error_info,
    format_stack_trace,
    parse_exception,
    sanitize_error_message,
    get_error_context,
    calculate_error_hash,
    group_similar_errors,
    suggest_fixes,
    find_error_documentation
)

from PolyglotX.utils.decorators import (
    handle_exceptions,
    translate_errors,
    retry_on_error,
    fallback_on_error,
    log_exceptions,
    measure_exception_time,
    suppress_exceptions,
    transform_exception,
    validate_exception,
    notify_on_exception
)

from PolyglotX.translators.engine_manager import (
    TranslationEngine,
    GoogleEngine,
    DeepLEngine,
    LibreEngine,
    MyMemoryEngine,
    PonsEngine,
    LingueeEngine,
    YandexEngine,
    BingEngine,
    PapagoEngine
)

from PolyglotX.cli.commands import (
    translate_command,
    test_command,
    benchmark_command,
    config_command,
    demo_command,
    export_command,
    import_command,
    validate_command,
    optimize_command,
    monitor_command
)

__all__ = [
    'arbe', 'tr', 'ja', 'zh', 'ku', 'es', 'hi', 'fr', 'ru', 'de', 'pt',
    'ExceptionHandler', 'GlobalExceptionHandler', 'ErrorTranslator',
    'TracebackTranslator', 'ContextualErrorHandler', 'AsyncExceptionHandler',
    'ThreadSafeExceptionHandler', 'ChainedExceptionHandler',
    'FilteredExceptionHandler', 'LoggingExceptionHandler',
    'Translator', 'MultiEngineTranslator', 'CachedTranslator',
    'BatchTranslator', 'OfflineTranslator', 'AdaptiveTranslator',
    'ContextAwareTranslator', 'TechnicalTranslator', 'SmartTranslator',
    'ErrorFormatter', 'ColoredErrorFormatter', 'HTMLErrorFormatter',
    'JSONErrorFormatter', 'XMLErrorFormatter', 'MarkdownErrorFormatter',
    'PlainTextErrorFormatter', 'RichErrorFormatter', 'CompactErrorFormatter',
    'VerboseErrorFormatter', 'OutputHandler', 'ConsoleOutputHandler',
    'FileOutputHandler', 'SyslogOutputHandler', 'EmailOutputHandler',
    'WebhookOutputHandler', 'DatabaseOutputHandler', 'StreamOutputHandler',
    'BufferedOutputHandler', 'AsyncOutputHandler', 'detect_language',
    'extract_error_info', 'format_stack_trace', 'parse_exception',
    'sanitize_error_message', 'get_error_context', 'calculate_error_hash',
    'group_similar_errors', 'suggest_fixes', 'find_error_documentation',
    'handle_exceptions', 'translate_errors', 'retry_on_error',
    'fallback_on_error', 'log_exceptions', 'measure_exception_time',
    'suppress_exceptions', 'transform_exception', 'validate_exception',
    'notify_on_exception', 'TranslationEngine', 'GoogleEngine',
    'DeepLEngine', 'LibreEngine', 'MyMemoryEngine', 'PonsEngine',
    'LingueeEngine', 'YandexEngine', 'BingEngine', 'PapagoEngine',
    'translate_command', 'test_command', 'benchmark_command',
    'config_command', 'demo_command', 'export_command', 'import_command',
    'validate_command', 'optimize_command', 'monitor_command'
]
