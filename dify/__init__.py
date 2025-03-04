"""
Dify SDK - Dify AI 平台的 Python SDK

提供与 Dify AI 平台交互的功能，包括应用管理、对话管理等。
"""

from .app import DifyApp
from .http import AdminClient, ApiClient

class Dify(object):
    def __init__(self, admin_client: AdminClient, api_client: ApiClient):
        self.app = DifyApp(admin_client, api_client)


__version__ = "0.1.0"
__all__ = ["Dify"]
