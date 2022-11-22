# Library's
from dataclasses import dataclass, field
from typing import List, Any

# Drivers
from core.driver.basemodel import baseModel, typeInput, export_model

# Models
from core.models.enigma import enigmaRotor

# Helpers
from core.helpers.scrambler import scrambler, scrambleSetting
from core.helpers.ascii_scope import ascii_scope, asciiSetting


@dataclass
class enigma(baseModel):
    # Vars for the inherited model class
    name: str = field(default='Enigma', init=False)
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

    def __hidden_enigma(self, content: str, rotor_func) -> str:
        if len(content) > 1:
            raise TypeError("to many chars")

        self.advanceRotors()

        index = self.ascii_scope.getIndex(content)
        for rotor in list(reversed(self.rotors)) + self.rotors[1:]:
            index = rotor_func(rotor, index)

        return self.ascii_scope.scope[index]

    def encrypt(self, content: str) -> str:
        return self.__hidden_enigma(content, lambda rotor, index: rotor.getPosition(index))

    def decrypt(self, content: str) -> str:
        return self.__hidden_enigma(content, lambda rotor, index: rotor.getPositionReverse(index))

    def reset(self) -> None:
        for rotor in self.rotors:
            rotor.reset()

    def __export__(self) -> List[Any]:
        return [
            export_model(self.ascii_scope),
            [export_model(rotor) for rotor in self.rotors]
        ]


# Standard model variables
MAIN_MODULE = enigma
MODULE_ATTRIBUTES = [ascii_scope, enigmaRotor]


if __name__ == '__main__':
    eni = enigma(
        ascii_scope(asciiSetting.lettersLower, extra_scope_chars=None)
    )

    # msg = 'hallo'
    msg = 'abcdefghijklmnopqrstuvwxyz'

    enc = ''
    for char in msg:
        enc += eni.encrypt(char)

    eni.reset()
    eni.advanceRotors()

    enc2 = ''
    for char in msg:
        enc2 += eni.encrypt(char)

    eni.reset()

    dec = ''
    for char in enc:
        dec += eni.decrypt(char)

    eni.reset()
    eni.advanceRotors()

    dec2 = ''
    for char in enc2:
        dec2 += eni.decrypt(char)

    print(msg, enc, enc2, dec, dec2, sep='\n')
