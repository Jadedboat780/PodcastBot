from typing import Literal

class TranslatorRunner:
	def get(self, path: str, **kwargs) -> str: ...

	message: Message
	button: Button

class Message:
	@staticmethod
	def welcome() -> Literal["""Welcome message"""]: ...
	@staticmethod
	def help() -> Literal["""Help message"""]: ...

class Button:
	@staticmethod
	def start() -> Literal["""Button start"""]: ...
	@staticmethod
	def help() -> Literal["""Button help"""]: ...
	@staticmethod
	def source() -> Literal["""Button source"""]: ...
