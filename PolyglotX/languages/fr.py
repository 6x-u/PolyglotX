from PolyglotX.core.exception_handler import ExceptionHandler


class FrenchExceptionHandler(ExceptionHandler):
    def __init__(self, show_credits: bool = True, auto_exit: bool = True, **kwargs):
        super().__init__(language='fr', show_credits=show_credits, auto_exit=auto_exit)
        self.install()


fr = FrenchExceptionHandler()
