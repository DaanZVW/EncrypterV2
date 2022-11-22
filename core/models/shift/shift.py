# Library's
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseModel, typeInput, export_model, attr_types

# Helpers
from core.helpers.scrambler import scrambler
from core.helpers.ascii_scope import ascii_scope, asciiSetting


@dataclass
class shift(baseModel):
    """
    Superclass vars
    """
    # Vars for the inherited model class
    name: str = field(default='shift', init=False)
    type: typeInput = field(default=typeInput.char, init=False)

    """ 
    Model vars 
    """
    # Amount of shift it will apply to a char
    shift_amount: int = field(default=0)
    # Setting which the model follows
    ascii_scope: 'ascii_scope' = field(default_factory=lambda: ascii_scope(asciiSetting.printable))
    # Set scrambler if given
    scrambler: 'scrambler' = field(default=None)

    def __post_init__(self):
        if not isinstance(self.ascii_scope, ascii_scope):
            raise TypeError("Ascii_scope is not of type ascii_type")

        if self.scrambler is not None:
            if isinstance(self.scrambler, scrambler):
                self.ascii_scope.scope = self.scrambler.scramble(self.ascii_scope.scope)
            else:
                raise TypeError(f'scramble_scope variable is of incorrect type: {self.scrambler}')

    def __hidden_shift(self, content: str, amount: int) -> str:
        index = self.ascii_scope.getIndex(content)
        move = (amount % len(self.ascii_scope.scope)) + index
        length_scope = len(self.ascii_scope.scope)

        if move < 0:
            move += length_scope
        elif move >= length_scope:
            move -= length_scope

        return self.ascii_scope.scope[move]

    def encrypt(self, content: str) -> str:
        return self.__hidden_shift(content, self.shift_amount)

    def decrypt(self, content: str) -> str:
        return self.__hidden_shift(content, -self.shift_amount)

    def __export__(self) -> List[Any]:
        return [
            self.shift_amount,
            export_model(self.ascii_scope),
            export_model(self.scrambler)
        ]


# Standard model variables
MAIN_MODULE = shift
MODULE_ATTRIBUTES = [int, ascii_scope, scrambler]

