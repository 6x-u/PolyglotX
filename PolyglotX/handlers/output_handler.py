import sys
import os
import json
import smtplib
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class OutputHandler:
    def __init__(self, language: str = 'ar'):
        self.language = language
        
    def handle(self, message: str):
        raise NotImplementedError


class ConsoleOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', stream=None):
        super().__init__(language)
        self.stream = stream or sys.stderr
        
    def handle(self, message: str):
        print(message, file=self.stream)
        
    def handle_error(self, error_info: Dict[str, Any]):
        self.handle(f"{error_info['type']}: {error_info['message']}")
    
    def handle_with_color(self, message: str, color_code: str = '\033[91m'):
        reset_code = '\033[0m'
        self.handle(f"{color_code}{message}{reset_code}")


class FileOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', filepath: str = 'errors.log'):
        super().__init__(language)
        self.filepath = filepath
        
    def handle(self, message: str):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
    
    def handle_error(self, error_info: Dict[str, Any]):
        self.handle(f"{error_info['type']}: {error_info['message']}")
    
    def clear_log(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class SyslogOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', server: str = 'localhost', port: int = 514):
        super().__init__(language)
        self.server = server
        self.port = port
        
    def handle(self, message: str):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (self.server, self.port))
        sock.close()


class EmailOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', smtp_server: str = 'smtp.gmail.com', 
                 smtp_port: int = 587, sender: str = '', password: str = '', 
                 recipients: Optional[List[str]] = None):
        super().__init__(language)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
        self.recipients = recipients or []
        
    def handle(self, message: str):
        if not self.recipients:
            return
        
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = f'Error Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)
            server.quit()
        except Exception:
            pass


class WebhookOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', webhook_url: str = ''):
        super().__init__(language)
        self.webhook_url = webhook_url
        
    def handle(self, message: str):
        if not self.webhook_url:
            return
        
        payload = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'language': self.language
        }
        
        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception:
            pass
    
    def handle_error(self, error_info: Dict[str, Any]):
        payload = {
            'error': error_info,
            'timestamp': datetime.now().isoformat(),
            'language': self.language
        }
        
        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception:
            pass


class DatabaseOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', connection_string: str = ''):
        super().__init__(language)
        self.connection_string = connection_string
        
    def handle(self, message: str):
        pass
    
    def handle_error(self, error_info: Dict[str, Any]):
        pass


class StreamOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', stream=None):
        super().__init__(language)
        self.stream = stream or sys.stdout
        
    def handle(self, message: str):
        self.stream.write(message + '\n')
        self.stream.flush()


class BufferedOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar', buffer_size: int = 100):
        super().__init__(language)
        self.buffer_size = buffer_size
        self.buffer = []
        
    def handle(self, message: str):
        self.buffer.append(message)
        
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        for message in self.buffer:
            print(message)
        self.buffer.clear()
    
    def get_buffer(self) -> List[str]:
        return self.buffer.copy()


class AsyncOutputHandler(OutputHandler):
    def __init__(self, language: str = 'ar'):
        super().__init__(language)
        self.queue = []
        
    async def handle_async(self, message: str):
        self.queue.append(message)
        await self._process_queue()
    
    async def _process_queue(self):
        while self.queue:
            message = self.queue.pop(0)
            print(message)
    
    def handle(self, message: str):
        self.queue.append(message)
