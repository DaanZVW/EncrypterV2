# Library's
from enum import Enum
from hashlib import sha1
from base64 import urlsafe_b64encode
from dataclasses import dataclass, field
from typing import List, Any, Union, Dict, NoReturn


def id_algorithm(str_input: str) -> bytes:
    """
    Get an identifier hash of a given input
    :param str_input: Input that needs to be hashed
    :return: Hashed input
    """
    if isinstance(str_input, str):
        str_input = str_input.encode('utf-8')

    return urlsafe_b64encode(
        sha1(str_input).digest()
    )


class typeInput(Enum):
    """
    Length of input the model wants
    """
    char = 0
    all = 1
    other = 2


@dataclass
class base:
    """
    Base class for manipulating/helping to manipulate data
    When deriving from this class you can use the following 2 functions:
    1. Exporting and importing models
    2. Can be used as addition to the encrypter models
    """
    # Name of the model. Should be unique, but can be avoided by using a different nonce
    name: str

    # Number only used once. This helps to keep a model identifiable when exported.
    nonce: int = field(init=False, default=0)

    # Identifier of a base.
    id: bytes = field(default=None, init=False)

    def __post_init__(self) -> NoReturn:
        """
        Fallback for if __post_init__ is not defined.
        This will only update the id with the update_id() function
        """
        self.update_id()

    def __export__(self) -> List[Any]:
        """
        Custom magic method for exporting models
        Return all the variables needed to recreate the model
        :return: List with values for init
        """
        raise TypeError("This model can't be exported")

    def update_id(self) -> NoReturn:
        """
        Get the ID of model by returning hash of key attributes
        :return: (HEX) Hash (md5) in string format
        """
        self.id = id_algorithm(self.name + str(self.nonce))


@dataclass
class baseHelper(base):
    """
    baseHelper defines a class that can help a model perform tasks but shouldn't be used in itself as a model.
    """
    pass


@dataclass
class baseModel(base):
    """
    baseModel defines a base for a model which can encrypt and decrypt data. The type of input data is defined here
    so the encrypter wrapper class knows how to feed the model correctly.
    """
    type: typeInput

    def update_id(self) -> NoReturn:
        """
        Redefine the function so that it includes the typeInput variable
        ================================================================
        Get the ID of model by returning hash of key attributes
        :return: (HEX) Hash (md5) in string format
        """
        self.id = id_algorithm(self.name + str(self.nonce) + str(typeInput))

    def encrypt(self, content: bytes) -> bytes:
        """
        Encrypt the input that is given
        :param content: bytes you want encrypted
        :return: encrypted input
        """
        raise TypeError("This model isn't capable to encrypt")

    def decrypt(self, content: bytes) -> bytes:
        """
        Decrypt the input that is given
        :param content: bytes you want decrypted
        :return: decrypted input
        """
        raise TypeError("This model isn't capable to decrypt")

    def reset(self, after_encryption: bool) -> None:
        """
        Reset the model. Define if needed. Will be called after every encrypt or decrypt call
        :param after_encryption: If the reset call has been done after the encrypt() function
        """
        pass


def export_model(model: base) -> Union[Dict[str, Any], None]:
    """
    Function for exporting a model. Only should be used with the __export__() function
    :param model: model to export
    :return: Dict with ID and Attributes
    """
    if model is None:
        return None
    return {'id': model.id, 'attributes': model.__export__()}


