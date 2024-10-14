class UrlWrong(Exception):
	"""Incorrect url"""

	def __init__(self, message: str | None = None):
		super().__init__(message)


class UrlToStream(Exception):
	"""The url leads to a direct stream"""

	def __init__(self, message: str | None = None):
		super().__init__(message)


class LargeFile(Exception):
	"""The file is too large to send"""

	def __init__(self, message: str | None = None):
		super().__init__(message)
