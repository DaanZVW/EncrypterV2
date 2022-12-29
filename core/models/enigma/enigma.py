# Library's
from dataclasses import dataclass, field
from typing import List, Any

# Drivers
from core.driver.encoder import export_model, import_model
from core.driver.basemodel import baseModel, typeInput

# Models
from core.models.enigma import enigmaRotor

# Helpers
from core.helpers.ascii_scope import ascii_scope, asciiSetting


@dataclass
class enigma(baseModel):
    # Vars for the inherited model class
    name: str = field(default='model.enigma.enigma', init=False)
    type: typeInput = field(default=typeInput.char, init=False)

    ascii_scope: 'ascii_scope' = field(default_factory=lambda: ascii_scope(asciiSetting.printable))
    rotors: List[enigmaRotor] = field(default_factory=list)

    def addRotor(self, rotor: enigmaRotor):
        if not isinstance(rotor, enigmaRotor):
            raise TypeError("Given rotor is not of type 'enigmaRotor'")

        self.rotors.append(rotor)

    def advanceRotors(self):
        for rotor in reversed(self.rotors):
            if rotor.advanceRotor():
                break

    def __hidden_enigma(self, content: bytes, rotor_func) -> bytes:
        self.advanceRotors()

        index = self.ascii_scope.get_index(content)
        for rotor in list(reversed(self.rotors)) + self.rotors[1:]:
            index = rotor_func(rotor, index)

        return self.ascii_scope.scope[index].to_bytes(1, 'little')

    def encrypt(self, content: bytes) -> bytes:
        return self.__hidden_enigma(content, lambda rotor, index: rotor.getPosition(index))

    def decrypt(self, content: bytes) -> bytes:
        return self.__hidden_enigma(content, lambda rotor, index: rotor.getPositionReverse(index))

    def reset(self, after_encryption: bool) -> None:
        for rotor in self.rotors:
            rotor.reset()

    @staticmethod
    def __export__(model: 'enigma') -> List[Any]:
        return [
            export_model(model.ascii_scope),
            [export_model(rotor) for rotor in model.rotors]
        ]

    @staticmethod
    def __import__(attributes: List[Any]) -> 'enigma':
        return enigma(
            ascii_scope=import_model(attributes[0]),
            rotors=[import_model(attrs) for attrs in attributes[1]]
        )


# Standard model variables
MAIN_MODULE = enigma


