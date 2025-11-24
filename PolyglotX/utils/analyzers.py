import re
from typing import Dict, Any, List, Tuple
from collections import Counter


class ErrorAnalyzer:
    def __init__(self):
        self.error_patterns = self._init_patterns()
        
    def _init_patterns(self) -> Dict[str, str]:
        return {
            'file_not_found': r"No such file or directory: '([^']+)'",
            'import_error': r"No module named '([^']+)'",
            'attribute_error': r"'([^']+)' object has no attribute '([^']+)'",
            'name_error': r"name '([^']+)' is not defined",
            'type_error': r"unsupported operand type\(s\) for ([^:]+): '([^']+)' and '([^']+)'"
        }
    
    def analyze_error(self, error_message: str) -> Dict[str, Any]:
        analysis = {
            'pattern_matches': [],
            'suggested_fixes': [],
            'severity': 'unknown'
        }
        
        for pattern_name, pattern in self.error_patterns.items():
            match = re.search(pattern, error_message)
            if match:
                analysis['pattern_matches'].append({
                    'pattern': pattern_name,
                    'matches': match.groups()
                })
        
        return analysis
    
    def get_error_frequency(self, errors: List[Exception]) -> Dict[str, int]:
        error_types = [type(e).__name__ for e in errors]
        return dict(Counter(error_types))
    
    def find_common_root_cause(self, errors: List[Exception]) -> str:
        if not errors:
            return 'No errors to analyze'
        
        error_types = [type(e).__name__ for e in errors]
        most_common = Counter(error_types).most_common(1)[0][0]
        
        return f"Most common error type: {most_common}"


class StackAnalyzer:
    def analyze_stack_depth(self, tb: Any) -> int:
        depth = 0
        while tb is not None:
            depth += 1
            tb = tb.tb_next
        return depth
    
    def find_recursive_calls(self, tb: Any) -> List[str]:
        functions = []
        while tb is not None:
            functions.append(tb.tb_frame.f_code.co_name)
            tb = tb.tb_next
        
        recursive = []
        function_counts = Counter(functions)
        for func, count in function_counts.items():
            if count > 1:
                recursive.append(func)
        
        return recursive
    
    def extract_call_chain(self, tb: Any) -> List[Dict[str, Any]]:
        chain = []
        while tb is not None:
            frame = tb.tb_frame
            chain.append({
                'function': frame.f_code.co_name,
                'filename': frame.f_code.co_filename,
                'lineno': tb.tb_lineno
            })
            tb = tb.tb_next
        return chain
