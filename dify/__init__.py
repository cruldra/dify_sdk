"""
Dify SDK - Dify AI 平台的 Python SDK

提供与 Dify AI 平台交互的功能，包括应用管理、对话管理等。
"""

from .app import DifyApp
from .http import AdminClient, ApiClient
from .llm import DifyLLM


class Dify(object):
    def __init__(self, admin_client: AdminClient):
        self.app = DifyApp(admin_client)
        self.llm = DifyLLM(admin_client)


__version__ = "0.1.0"
__all__ = ["Dify", "AdminClient"]
