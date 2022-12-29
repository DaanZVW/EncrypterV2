# Library's
from dataclasses import dataclass, field
from typing import List, Callable, Any, Union

# Drivers
from core.driver.basemodel import baseModel, typeInput
from core.driver.encoder import export_model, import_model


@dataclass
class encrypter:
    def __init__(self, *models: baseModel):
        self.models: List[baseModel] = list()
        for model in models:
            self.addModel(model)

    def addModel(self, model) -> bool:
        if not isinstance(model, baseModel):
            raise TypeError("Added model must be of type 'baseModel', not of type {}".format(model))

        self.models.append(model)
        return True

    @staticmethod
    def __hidden_encrypt(
            content: bytearray,
            model: baseModel,
            function: Callable[[baseModel, Union[bytearray, int]], bytearray]
    ) -> bytearray:

        new_content = bytearray()
        if model.type == typeInput.char:
            for letter in content:
                new_content += function(model, letter)

        elif model.type == typeInput.all:
            new_content += function(model, content)

        else:
            raise TypeError("typeInput.other is not supported yet")

        return new_content

    def encrypt(self, content: bytes) -> bytes:
        content = bytearray(content)

        for model in self.models:
            content = self.__hidden_encrypt(content, model, lambda m, c: m.encrypt(c))
            model.reset(after_encryption=True)
        return bytes(content)

    def decrypt(self, content: bytes) -> bytes:
        content = bytearray(content)

        for model in reversed(self.models):
            content = self.__hidden_encrypt(content, model, lambda m, c: m.decrypt(c))
            model.reset(after_encryption=False)
        return bytes(content)

    def export_encrypter(self) -> List[Any]:
        return [export_model(model) for model in self.models]

    def import_encrypter(self, models: List[Any]) -> bool:
        for model in models:
            self.addModel(import_model(model))
        return True

    def __repr__(self) -> str:
        model_info = [model.__repr__() for model in self.models]
        return "Encrypter object containing:\n" \
               "============================\n" + \
               "\n".join(model_info)

