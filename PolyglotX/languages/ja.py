from PolyglotX.core.exception_handler import ExceptionHandler


class JapaneseExceptionHandler(ExceptionHandler):
    def __init__(self, show_credits: bool = True, auto_exit: bool = True, **kwargs):
        super().__init__(language='ja', show_credits=show_credits, auto_exit=auto_exit)
        self.install()


ja = JapaneseExceptionHandler()
