import os
from typing import Optional
from pathlib import Path

from dify.http import AdminClient
from .schemas import UploadFile


class DifyFile:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def upload(self, file_path: str, source: str = "datasets") -> UploadFile:
        """上传文件到Dify平台

        Args:
            file_path: 文件路径
            source: 文件来源，默认为datasets

        Returns:
            FileUploadResponse: 文件上传响应对象，包含文件ID等信息

        Raises:
            ValueError: 当文件路径为空或文件不存在时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        if not file_path:
            raise ValueError("文件路径不能为空")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise ValueError(f"文件不存在: {file_path}")

        # 获取文件名
        file_name = os.path.basename(file_path)

        # 打开文件并准备上传
        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            
            # 发送请求上传文件
            response_data = await self.admin_client.upload(
                f"/files/upload?source={source}",
                files=files
            )

        # 返回文件上传响应对象
        return UploadFile(**response_data)


__all__ = ["DifyFile"]

