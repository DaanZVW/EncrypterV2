# Library's
from enum import Enum
from hashlib import md5
from dataclasses import dataclass, field
from typing import List, Any, Union, Dict


class typeInput(Enum):
    char = 0
    all = 1
    other = 2


@dataclass
class base:
    """
    Base class.
    When using this class as base you will have the following support:
    1. If used correctly, automatic support for exporting and importing your model
    2. Model can be added to the encrypter class
    """
    name: str
    nonce: int = field(init=False, default=0)

    def __export__(self) -> List[Any]:
        """
        Custom magic method for exporting models
        Return all the variables needed to recreate the model
        :return: List with values for init
        """
        raise TypeError("This model can't be exported")


@dataclass
class baseHelper(base):
    def getID(self) -> str:
        """
        Get the ID of model by returning hash of key attributes
        :return: (HEX) Hash (md5) in string format
        """
        attributes = [self.name, str(self.nonce)]
        return md5("".join(attributes).encode('utf-8')).hexdigest()


@dataclass
class baseModel(base):
    type: typeInput

    def encrypt(self, content: str) -> str:
        """
        Encrypt the input that is given
        :param content: string you want encrypted
        :return: encrypted input
        """
        raise TypeError("This model isn't capable to encrypt")

    def decrypt(self, content: str) -> str:
        """
        Decrypt the input that is given
        :param content: string you want decrypted
        :return: decrypted input
        """
        raise TypeError("This model isn't capable to decrypt")

    def getID(self) -> str:
        """
        Get the ID of model by returning hash of key attributes
        :return: (HEX) Hash (md5) in string format
        """
        attributes = [self.name, str(self.type), str(self.nonce)]
        return md5("".join(attributes).encode('utf-8')).hexdigest()

    def reset(self) -> bool:
        """
        Reset the model. Define if needed. Will be called after every encrypt or decrypt call
        :return:
        """
        pass


def export_model(model: base) -> Union[Dict[str, Any], None]:
    if model is None:
        return None
    return {'id': model.getID(), 'attributes': model.__export__()}


def attr_types(model: base) -> List[type]:
    return [type(attr) for attr in model.__export__()]
