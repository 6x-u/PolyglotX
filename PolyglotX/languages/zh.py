from PolyglotX.core.exception_handler import ExceptionHandler


class ChineseExceptionHandler(ExceptionHandler):
    def __init__(self, show_credits: bool = True, auto_exit: bool = True, **kwargs):
        super().__init__(language='zh-CN', show_credits=show_credits, auto_exit=auto_exit)
        self.install()


zh = ChineseExceptionHandler()
