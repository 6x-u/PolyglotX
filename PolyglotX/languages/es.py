from PolyglotX.core.exception_handler import ExceptionHandler


class SpanishExceptionHandler(ExceptionHandler):
    def __init__(self, show_credits: bool = True, auto_exit: bool = True, **kwargs):
        super().__init__(language='es', show_credits=show_credits, auto_exit=auto_exit)
        self.install()


es = SpanishExceptionHandler()
