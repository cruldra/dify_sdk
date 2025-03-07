from dify.http import AdminClient
from .schemas import DataSetCreatePayloads, DataSetCreateResponse

class DifyDataset:
    def __init__(self, admin_client: AdminClient) -> None:
        self.admin_client = admin_client

    async def create(self, payload: DataSetCreatePayloads) -> DataSetCreateResponse:
        pass

