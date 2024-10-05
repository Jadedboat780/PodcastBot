from aiobotocore.session import get_session, AioSession, AioBaseClient
import aiofiles

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from bot.config import config


class Storage:
    __slots__ = ("config", "bucket_name", "session")

    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name: str = bucket_name
        self.session: AioSession = get_session()

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient, None]:
        """Getting the S3 client"""
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str, object_key: str) -> None:
        """Upload file in S3"""
        async with self.get_client() as client:
            async with aiofiles.open(file_path, "rb") as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    Body=await file.read(),
                )

    async def download_file(self, object_key: str, destination_path: str) -> None:
        """Upload file from S3"""
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=object_key)
            data = await response["Body"].read()
            async with aiofiles.open(destination_path, "wb") as file:
                await file.write(data)

    async def delete_file(self, object_key: str):
        """Delete file from S3"""
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_key)

    async def list_files(self) -> list[dict]:
        """Getting a list of files from S3"""
        async with self.get_client() as client:
            paginator = client.get_paginator("list_objects_v2")
            file_list = []
            async for page in paginator.paginate(Bucket=self.bucket_name):
                file_list.extend(page.get("Contents", []))
            return file_list

    def __repr__(self):
        return f'Storage(bucket_name="{self.bucket_name}")'


storage = Storage(
    access_key=config.access_key,
    secret_key=config.secret_key,
    endpoint_url=config.endpoint_url,
    bucket_name=config.bucket_name,
)
