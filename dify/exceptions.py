class DifyException(Exception):
    """Dify异常基类"""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"
