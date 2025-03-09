from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager

import aiofiles
import aiofiles.os as aos
from aiobotocore.session import AioBaseClient, AioSession, get_session

from bot.config import config


class Storage:
	__slots__ = ("config", "bucket_name", "session")

	def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
		self.config = {"aws_access_key_id": access_key, "aws_secret_access_key": secret_key, "endpoint_url": endpoint_url}
		self.bucket_name: str = bucket_name
		self.session: AioSession = get_session()

	@asynccontextmanager
	async def get_client(self) -> AsyncGenerator[AioBaseClient, None]:
		"""Getting the S3 client"""
		async with self.session.create_client("s3", **self.config) as client:
			yield client

	async def upload_file(self, path: str, object_key: str, is_delete: bool = False) -> int:
		"""Uploads the file in S3 and optionally deletes it"""
		file_path = f"{path}/{object_key}"
		file_size = await aos.path.getsize(file_path)

		async with self.get_client() as client:
			async with aiofiles.open(file_path, "rb") as file:
				await client.put_object(
					Bucket=self.bucket_name,
					Key=object_key,
					Body=await file.read(),
				)

		if is_delete:
			await aos.remove(file_path)

		return file_size

	async def download_file(self, object_key: str, destination_path: str) -> None:
		"""Downloads the file from S3"""
		async with self.get_client() as client:
			response = await client.get_object(Bucket=self.bucket_name, Key=object_key)
			data = await response["Body"].read()
			async with aiofiles.open(destination_path, "wb") as file:
				await file.write(data)

	async def delete_file(self, object_key: str):
		"""Delete file from S3"""
		async with self.get_client() as client:
			await client.delete_object(Bucket=self.bucket_name, Key=object_key)

	async def list_files(self) -> Generator[str, None, None]:
		"""Getting a list of files from S3"""
		files_info: list[dict] = []

		async with self.get_client() as client:
			paginator = client.get_paginator("list_objects_v2")
			async for page in paginator.paginate(Bucket=self.bucket_name):
				files_info.extend(page.get("Contents", []))

		files_name = (f["Key"] for f in files_info)
		return files_name

	async def file_link(self, filename: str) -> str | None:
		"""Returns link to file by filename"""
		files = await self.list_files()
		if filename in files:
			return f"{config.domain}/{filename}"
		else:
			return None

	def __repr__(self):
		return f'Storage(bucket_name="{self.bucket_name}")'


storage = Storage(
	access_key=config.access_key,
	secret_key=config.secret_key,
	endpoint_url=config.endpoint_url,
	bucket_name=config.bucket_name,
)
