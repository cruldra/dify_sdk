"""
Dify SDK - Dify AI 平台的 Python SDK

提供与 Dify AI 平台交互的功能，包括应用管理、对话管理等。
"""

from .app import DifyApp
from .http import AdminClient, ApiClient
from .llm import DifyLLM
from .file import DifyFile
from .dataset import DifyDataset
from .tag import DifyTag


class Dify(object):
    def __init__(self, admin_client: AdminClient):
        self.app = DifyApp(admin_client)
        self.llm = DifyLLM(admin_client)
        self.file = DifyFile(admin_client)
        self.dataset = DifyDataset(admin_client)
        self.tag = DifyTag(admin_client)
__version__ = "0.1.0"
__all__ = ["Dify", "AdminClient"]
