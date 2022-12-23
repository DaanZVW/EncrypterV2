# Library's
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseModel, typeInput, export_model

# Helpers
from core.helpers.scrambler import scrambler
from core.helpers.ascii_scope import ascii_scope


@dataclass
class shift(baseModel):
    """
    Model for shifting variables in the ascii table.


    shift_amount:
        Description: How many shifts a char will be encrypted with
        Type       : int
        Default    : 0
        NOTE       : Can be positive and negative
    ascii_scope:
        Description: Scope of all the ascii letters it allows
        Type       : helpers.ascii_scope
        Default    : default helpers.ascii_scope
        NOTE       : -
    scrambler:
        Description: If defined, will scramble the helpers.ascii_scope for extra encryption
        Type       : helpers.scrambler
        Default    : None
        NOTE       : -
    """
    # Superclass variables
    name: str = field(default='model.shift', init=False)
    type: typeInput = field(default=typeInput.char, init=False)

    # Model specific settings
    shift_amount: int = field(default=0)
    ascii_scope: 'ascii_scope' = field(default_factory=ascii_scope)
    scrambler: 'scrambler' = field(default=None)

    def __post_init__(self):
        """
        Function that should be used for checking the validity of the variables
        """
        # Check the ascii_scope variable
        if not isinstance(self.ascii_scope, ascii_scope):
            raise TypeError("Ascii_scope is not of type ascii_type")

        # If scrambler is set, try to scramble the ascii_scope
        if self.scrambler is not None:
            if not isinstance(self.scrambler, scrambler):
                raise TypeError(f'scramble_scope variable is of incorrect type: {self.scrambler}')

            self.ascii_scope.scope = self.scrambler.scramble(self.ascii_scope.scope)

        # Update the id when the object constructor is called
        self.update_id()

    def __hidden_shift(self, content: bytes, amount: int) -> bytes:
        """
        Internal shift function
        :param content: Char to shift
        :param amount: Amount to shift (can be negative)
        :return: Encrypted char
        """
        # Index the char of the ascii_scope
        index = self.ascii_scope.get_index(content)

        # Make sure that the shift amount is within the length of the ascii_scope
        length_scope = len(self.ascii_scope.scope)
        move = (amount % length_scope) + index

        # Keep the move var within 0 and length of ascii_scope
        if move < 0:
            move += length_scope
        elif move >= length_scope:
            move -= length_scope

        # Return the encrypted char
        return self.ascii_scope.scope[move].to_bytes(1, 'little')

    def encrypt(self, content: bytes) -> bytes:
        """
        Encrypt the input that is given
        :param content: string you want encrypted
        :return: encrypted input
        """
        return self.__hidden_shift(content, self.shift_amount)

    def decrypt(self, content: bytes) -> bytes:
        """
        Decrypt the input that is given
        :param content: string you want decrypted
        :return: decrypted input
        """
        return self.__hidden_shift(content, -self.shift_amount)

    def __export__(self) -> List[Any]:
        """
        Custom magic method for exporting models
        Return all the variables needed to recreate the model
        :return: List with values for init
        """
        return [
            self.shift_amount,
            export_model(self.ascii_scope),
            export_model(self.scrambler)
        ]


# Standard model variables
MAIN_MODULE = shift
MODULE_ATTRIBUTES = [int, ascii_scope, scrambler]

