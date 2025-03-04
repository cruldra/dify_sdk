from ..http import AdminClient
from ..schemas import Pagination
from .schemas import App


class DifyApp:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def find_list(
        self,
        page: int = 1,
        limit: int = 100,
        mode: str = None,
        name: str = "",
        is_created_by_me: bool = False,
    ):
        """从 Dify 分页获取应用列表

        Args:
            page: 页码，默认为1
            limit: 每页数量限制，默认为100
            mode: 应用模式过滤，可选
            name: 应用名称过滤，默认为空字符串
            is_created_by_me: 是否只返回由我创建的应用，默认为False

        Returns:
            Pagination[App]: 分页的应用列表
        """

        params = {
            "page": page,
            "limit": limit,
            "name": name,
            "is_created_by_me": is_created_by_me,
        }

        if mode:
            params["mode"] = mode

        response_data = await self.admin_client.get(
            "/apps",
            params=params,
        )

        return Pagination[App].model_validate(response_data)

    def find_by_id(self):
        pass
