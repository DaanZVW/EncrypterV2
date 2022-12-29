# Library's
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.encoder import export_model, import_model
from core.driver.basemodel import baseHelper, typeInput

# Helpers
from core.helpers.scrambler import scrambler


@dataclass
class enigmaRotor(baseHelper):
    """
    Superclass vars
    """
    # Vars for the inherited model class
    name: str = field(default='model.enigma.enigmaRotor', init=False)
    type: typeInput = field(default=typeInput.char, init=False)

    rotorSize: int = field(default=0)
    rotorPosition: int = field(default=0)
    rotorOffset: int = field(default=0)

    scrambler: 'scrambler' = field(default=None)

    rotor: bytearray = field(init=False)

    __init_rotorPosition: int = field(init=False, repr=False)

    def __post_init__(self):
        # Update the id when the object constructor is called
        self.update_id()

        self.rotor = bytearray(range(self.rotorSize))

        if isinstance(self.scrambler, scrambler):
            self.rotor = self.scrambler.scramble(self.rotor)
        elif self.scrambler is not None:
            raise AttributeError(f"given scrambler is of unknown type '{type(self.scrambler)}'")

        if self.rotorOffset != 0:
            if abs(self.rotorOffset) > self.rotorSize:
                raise ValueError("rotorOffset is larger than rotorSize")
            self.rotor = self.rotor[self.rotorOffset:] + self.rotor[:self.rotorOffset]

        self.__init_rotorPosition = self.rotorPosition

    def getPosition(self, position: int) -> int:
        index = (self.rotorPosition + position) % self.rotorSize
        return self.rotor[index]

    def getPositionReverse(self, position: int) -> int:
        return (self.rotor.index(position) - self.rotorPosition) % self.rotorSize

    def advanceRotor(self) -> bool:
        self.rotorPosition += 1
        if self.rotorPosition >= self.rotorSize:
            self.rotorPosition = 0
            return True
        return False

    def reset(self) -> None:
        self.rotorPosition = self.__init_rotorPosition
        self.__post_init__()

    @staticmethod
    def __export__(model: 'enigmaRotor') -> List[Any]:
        return [
            model.rotorSize,
            model.__init_rotorPosition,
            model.rotorOffset,
            export_model(model.scrambler)
        ]

    @staticmethod
    def __import__(attributes: List[Any]) -> 'enigmaRotor':
        return enigmaRotor(
            rotorSize=attributes[0],
            rotorPosition=attributes[1],
            rotorOffset=attributes[2],
            scrambler=import_model(attributes[3])
        )


# Standard model variables
MAIN_MODULE = enigmaRotor

