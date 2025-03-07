from dify.http import AdminClient
from .schemas import LLM, LLMList


class DifyLLM:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def find_list(self) -> LLMList:
        response_data = await self.admin_client.get(
            "/workspaces/current/models/model-types/llm",
        )
        return LLMList(**response_data)


__all__ = ["DifyLLM"]