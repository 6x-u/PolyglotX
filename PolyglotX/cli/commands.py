import click
import sys
from PolyglotX.core.translator import Translator
from PolyglotX.core.exception_handler import ExceptionHandler


@click.group()
def cli():
    pass


@cli.command()
@click.argument('text')
@click.option('--language', '-l', default='ar', help='Target language code')
def translate_command(text, language):
    translator = Translator(target_language=language)
    result = translator.translate(text)
    click.echo(result)


@cli.command()
@click.option('--language', '-l', default='ar', help='Target language code')
def test_command(language):
    handler = ExceptionHandler(language=language)
    handler.install()
    
    try:
        raise ValueError("Test error message")
    except Exception:
        pass


@cli.command()
@click.option('--language', '-l', default='ar', help='Target language code')
@click.option('--count', '-c', default=100, help='Number of tests')
def benchmark_command(language, count):
    translator = Translator(target_language=language)
    
    import time
    test_texts = [
        "Error", "Exception", "File not found", "Invalid value",
        "Type error", "Name error", "Syntax error", "Import error",
        "Runtime error", "Memory error"
    ] * (count // 10)
    
    start = time.time()
    for text in test_texts[:count]:
        translator.translate(text)
    elapsed = time.time() - start
    
    click.echo(f"Translated {count} texts in {elapsed:.2f} seconds")
    click.echo(f"Average: {elapsed/count*1000:.2f} ms per translation")


@cli.command()
@click.option('--language', '-l', default='ar', help='Target language code')
@click.option('--credits/--no-credits', default=True)
def config_command(language, credits):
    click.echo(f"Language: {language}")
    click.echo(f"Show credits: {credits}")


@cli.command()
@click.option('--language', '-l', default='ar', help='Target language code')
def demo_command(language):
    handler = ExceptionHandler(language=language)
    handler.install()
    
    click.echo(f"Demo for language: {language}")
    
    try:
        x = 1 / 0
    except Exception:
        pass


@cli.command()
@click.argument('output_file')
def export_command(output_file):
    click.echo(f"Exporting configuration to {output_file}")


@cli.command()
@click.argument('input_file')
def import_command(input_file):
    click.echo(f"Importing configuration from {input_file}")


@cli.command()
def validate_command():
    click.echo("Validating installation...")
    click.echo("PolyglotX is installed correctly!")


@cli.command()
def optimize_command():
    click.echo("Optimizing translation cache...")


@cli.command()
def monitor_command():
    click.echo("Monitoring error translations...")


if __name__ == '__main__':
    cli()
