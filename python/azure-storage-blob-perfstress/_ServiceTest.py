import os

from azure.test.perfstress import PerfStressTest

from azure.storage.blob import BlobServiceClient as SyncBlobServiceClient
from azure.storage.blob.aio import BlobServiceClient as AsyncBlobServiceClient

class _ServiceTest(PerfStressTest):
    async def GlobalSetupAsync(self):
        await super().GlobalSetupAsync()

        connection_string = os.environ.get("STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise Exception("Undefined environment variable STORAGE_CONNECTION_STRING")

        if self.Arguments.max_single_put_size:
            self.service_client = SyncBlobServiceClient.from_connection_string(conn_str=connection_string, max_single_put_size=self.Arguments.max_single_put_size)
            self.async_service_client = AsyncBlobServiceClient.from_connection_string(conn_str=connection_string, max_single_put_size=self.Arguments.max_single_put_size)
        else:
            self.service_client = SyncBlobServiceClient.from_connection_string(conn_str=connection_string)
            self.async_service_client = SyncBlobServiceClient.from_connection_string(conn_str=connection_string)

        await self.async_service_client.__aenter__()

    async def GlobalCleanupAsync(self):
        await self.async_service_client.__aexit__()
        await super().GlobalCleanupAsync()

    @staticmethod
    def AddArguments(parser):
        super(_ServiceTest, _ServiceTest).AddArguments(parser)
        parser.add_argument('--max-single-put-size', nargs='?', type=int, help='Maximum size of blob uploading in single HTTP PUT.  Default is None.')