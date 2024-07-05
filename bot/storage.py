from aiobotocore.session import get_session, AioSession, AioBaseClient
import aiofiles
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from bot.config import config


class Storage:
    __slots__ = ('config', 'bucket_name', 'session')

    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name: str = bucket_name
        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient, None]:
        """Получение сессии"""
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_name: str):
        """Загрузка файла в хранилище"""
        async with self.get_client() as client:
            async with aiofiles.open(file_name, "rb") as file:
                await client.put_object(Bucket=self.bucket_name, Key=file_name, Body=await file.read())

    async def get_file(self, file_name: str, new_file: str):
        """Загрузка файла из хранилища"""
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=file_name)
            data = await response["Body"].read()
            async with aiofiles.open(new_file, "wb") as file:
                await file.write(data)

    async def delete_file(self, file_name: str):
        """Удаление файла из хранилища"""
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def __repr__(self):
        return f'Storage "{self.bucket_name}"'


storage = Storage(access_key=config.access_key,
                  secret_key=config.secret_key,
                  endpoint_url=config.endpoint_url,
                  bucket_name=config.bucket_name)
