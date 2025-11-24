import json
import yaml
from typing import Dict, Any, List


def exception_to_dict(exc: Exception) -> Dict[str, Any]:
    return {
        'type': type(exc).__name__,
        'message': str(exc),
        'args': list(exc.args) if exc.args else []
    }


def exception_to_json(exc: Exception) -> str:
    return json.dumps(exception_to_dict(exc), ensure_ascii=False, indent=2)


def exception_to_yaml(exc: Exception) -> str:
    return yaml.dump(exception_to_dict(exc), allow_unicode=True)


def traceback_to_list(tb: Any) -> List[str]:
    import traceback
    return traceback.format_tb(tb)


def traceback_to_string(tb: Any) -> str:
    return ''.join(traceback_to_list(tb))


def error_dict_to_string(error_dict: Dict[str, Any]) -> str:
    return f"{error_dict.get('type', 'Unknown')}: {error_dict.get('message', '')}"


def string_to_error_dict(error_string: str) -> Dict[str, Any]:
    if ':' in error_string:
        parts = error_string.split(':', 1)
        return {
            'type': parts[0].strip(),
            'message': parts[1].strip() if len(parts) > 1 else ''
        }
    return {'type': 'Unknown', 'message': error_string}
