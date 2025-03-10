from dify.http import AdminClient
from .schemas import WorkflowPublish


class DifyWorkflow:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def get_publish(self, app_id: str) -> WorkflowPublish:
        """获取工作流发布详情

        Args:
            app_id: 应用ID

        Returns:
            WorkflowPublish: 工作流发布详情

        Raises:
            ValueError: 当工作流ID为空时抛出
            httpx.HTTPStatusError: 当API请求失败时抛出
        """
        pass

__all__ = ["DifyWorkflow"]
