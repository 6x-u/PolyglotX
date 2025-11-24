from PolyglotX.core.exception_handler import ExceptionHandler


class TurkishExceptionHandler(ExceptionHandler):
    def __init__(self, show_credits: bool = True, auto_exit: bool = True, **kwargs):
        super().__init__(language='tr', show_credits=show_credits, auto_exit=auto_exit)
        self.install()


tr = TurkishExceptionHandler()
