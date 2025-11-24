import json
import html
from typing import Dict, Any, List
from colorama import Fore, Back, Style, init
from datetime import datetime

init(autoreset=True)


class ErrorFormatter:
    def __init__(self, language: str = 'ar'):
        self.language = language
        
    def format(self, error_info: Dict[str, Any]) -> str:
        return f"{error_info['type']}: {error_info['message']}"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = [self.format(error_info)]
        output.extend(traceback)
        return '\n'.join(output)


class ColoredErrorFormatter(ErrorFormatter):
    def __init__(self, language: str = 'ar', color_scheme: str = 'default'):
        super().__init__(language)
        self.color_scheme = color_scheme
        self._init_colors()
        
    def _init_colors(self):
        if self.color_scheme == 'default':
            self.error_color = Fore.RED
            self.warning_color = Fore.YELLOW
            self.info_color = Fore.CYAN
            self.success_color = Fore.GREEN
        elif self.color_scheme == 'dark':
            self.error_color = Fore.LIGHTRED_EX
            self.warning_color = Fore.LIGHTYELLOW_EX
            self.info_color = Fore.LIGHTCYAN_EX
            self.success_color = Fore.LIGHTGREEN_EX
    
    def format(self, error_info: Dict[str, Any]) -> str:
        error_type = f"{self.error_color}{error_info['type']}{Style.RESET_ALL}"
        error_msg = f"{Fore.WHITE}{error_info['message']}{Style.RESET_ALL}"
        return f"{error_type}: {error_msg}"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = []
        output.append(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        output.append(self.format(error_info))
        output.append(f"{Fore.CYAN}Traceback:{Style.RESET_ALL}")
        
        for line in traceback:
            output.append(f"{Fore.YELLOW}{line}{Style.RESET_ALL}")
        
        output.append(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        return '\n'.join(output)


class HTMLErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f'<div class="error"><span class="error-type">{html.escape(error_info["type"])}</span>: <span class="error-message">{html.escape(error_info["message"])}</span></div>'
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = ['<div class="error-container">']
        output.append(f'<h3 class="error-title">{html.escape(error_info["type"])}: {html.escape(error_info["message"])}</h3>')
        output.append('<div class="traceback">')
        
        for line in traceback:
            output.append(f'<pre>{html.escape(line)}</pre>')
        
        output.append('</div>')
        output.append('</div>')
        return '\n'.join(output)


class JSONErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return json.dumps({
            'error': {
                'type': error_info['type'],
                'message': error_info['message'],
                'timestamp': datetime.now().isoformat()
            }
        }, ensure_ascii=False, indent=2)
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        return json.dumps({
            'error': {
                'type': error_info['type'],
                'message': error_info['message'],
                'traceback': traceback,
                'timestamp': datetime.now().isoformat()
            }
        }, ensure_ascii=False, indent=2)


class XMLErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f'<error><type>{html.escape(error_info["type"])}</type><message>{html.escape(error_info["message"])}</message></error>'
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = ['<?xml version="1.0" encoding="UTF-8"?>']
        output.append('<error>')
        output.append(f'  <type>{html.escape(error_info["type"])}</type>')
        output.append(f'  <message>{html.escape(error_info["message"])}</message>')
        output.append('  <traceback>')
        
        for line in traceback:
            output.append(f'    <line>{html.escape(line)}</line>')
        
        output.append('  </traceback>')
        output.append(f'  <timestamp>{datetime.now().isoformat()}</timestamp>')
        output.append('</error>')
        return '\n'.join(output)


class MarkdownErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f"**{error_info['type']}**: {error_info['message']}"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = [f"## Error: {error_info['type']}\n"]
        output.append(f"**Message**: {error_info['message']}\n")
        output.append("### Traceback\n")
        output.append("```")
        output.extend(traceback)
        output.append("```")
        return '\n'.join(output)


class PlainTextErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f"{error_info['type']}: {error_info['message']}"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = []
        output.append('=' * 60)
        output.append(self.format(error_info))
        output.append('-' * 60)
        output.extend(traceback)
        output.append('=' * 60)
        return '\n'.join(output)


class RichErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f"[ERROR] {error_info['type']}: {error_info['message']} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = []
        output.append('╔' + '═' * 58 + '╗')
        output.append(f"║ ERROR: {error_info['type']:<48} ║")
        output.append('╠' + '═' * 58 + '╣')
        output.append(f"║ {error_info['message']:<56} ║")
        output.append('╠' + '═' * 58 + '╣')
        
        for line in traceback[:5]:
            if len(line) > 56:
                line = line[:53] + '...'
            output.append(f"║ {line:<56} ║")
        
        output.append('╚' + '═' * 58 + '╝')
        return '\n'.join(output)


class CompactErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        return f"[{error_info['type']}] {error_info['message']}"
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        tb_summary = traceback[-1] if traceback else 'No traceback'
        return f"[{error_info['type']}] {error_info['message']} | {tb_summary}"


class VerboseErrorFormatter(ErrorFormatter):
    def format(self, error_info: Dict[str, Any]) -> str:
        output = []
        output.append(f"Error Type: {error_info['type']}")
        output.append(f"Error Message: {error_info['message']}")
        output.append(f"Timestamp: {datetime.now().isoformat()}")
        output.append(f"Language: {self.language}")
        return '\n'.join(output)
    
    def format_with_traceback(self, error_info: Dict[str, Any], traceback: List[str]) -> str:
        output = []
        output.append("=" * 80)
        output.append("ERROR REPORT")
        output.append("=" * 80)
        output.append(self.format(error_info))
        output.append("")
        output.append("TRACEBACK:")
        output.append("-" * 80)
        output.extend(traceback)
        output.append("=" * 80)
        return '\n'.join(output)
