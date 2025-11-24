import click
from PolyglotX.core.translator import Translator
from PolyglotX.core.exception_handler import ExceptionHandler


class InteractiveMode:
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.translator = Translator(target_language=language)
        self.handler = ExceptionHandler(language=language)
        
    def run(self):
        self.handler.install()
        click.echo(f"Interactive mode started for language: {self.language}")
        click.echo("Type 'exit' to quit")
        
        while True:
            text = click.prompt("Enter text to translate", default="")
            
            if text.lower() == 'exit':
                break
            
            if text:
                result = self.translator.translate(text)
                click.echo(f"Translation: {result}")
        
        self.handler.uninstall()


def start_interactive(language: str = 'ar'):
    mode = InteractiveMode(language=language)
    mode.run()
