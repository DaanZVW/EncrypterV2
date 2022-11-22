# Library's
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseHelper, typeInput, export_model

# Helpers
from core.helpers.scrambler import scrambler, scrambleSetting


@dataclass
class enigmaRotor(baseHelper):
    """
    Superclass vars
    """
    # Vars for the inherited model class
    name: str = field(default='enigma.enigmaRotor', init=False)
    type: typeInput = field(default=typeInput.char, init=False)

    rotorSize: int = field(default=0)
    rotorPosition: int = field(default=0)
    rotorOffset: int = field(default=0)

    scrambler: 'scrambler' = field(default=None)

    rotor: List[int] = field(default_factory=list, init=False)

    __init_rotorPosition: int = field(init=False, repr=False)

    def __post_init__(self):
        self.rotor = list(range(self.rotorSize))

        if isinstance(self.scrambler, scrambler):
            self.rotor = self.scrambler.scramble(self.rotor)

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

    def __export__(self) -> List[Any]:
        return [
            self.rotorSize,
            self.__init_rotorPosition,
            self.rotorOffset,
            export_model(self.scrambler)
        ]


# Standard model variables
MAIN_MODULE = enigmaRotor
MODULE_ATTRIBUTES = [int, int, int, scrambler]


if __name__ == '__main__':
    rotorSize = 5
    a = enigmaRotor(
        rotorSize=rotorSize,
        rotorOffset=0,
        rotorPosition=0,
        scrambler=scrambler(scrambleSetting.customSeed, 4)
    )
    print(a)

    for i in range(rotorSize):
        result = a.getPosition(i)
        print(i, end=' ')
        print(result, end=' ')
        print(a.getPositionReverse(result))
    print()

    print(a.advanceRotor())
    print(a.getPosition(0))
    print(a.reset())
    print(a.getPosition(0))


