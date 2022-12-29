# Libraries
from typing import Type, Union
from dataclasses import dataclass


class EncrypterError(Exception):
    """Base exception for the encrypter framework"""


class ExporterError(EncrypterError):
    """Framework exception for export errors"""


class ImporterError(EncrypterError):
    """Framework exception for import errors"""


class FileError(EncrypterError):
    """Framework exception for file interacting errors"""
    def __init__(self, file_path: Union[str, None], comment: str):
        super().__init__(f"File '{file_path}': {comment}")


@dataclass
class raise_error:
    capture: Type[Exception]
    raise_exception: Union[Type[EncrypterError], EncrypterError]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        elif exc_type == self.capture:
            raise self.raise_exception from exc_val
        return False

