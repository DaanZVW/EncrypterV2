# Library's
from enum import Enum
from warnings import warn
from typing import List, Callable, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.encoder import export_model, import_model
from core.driver.basemodel import baseModel, typeInput

# Helpers
from core.helpers.scrambler import scrambler


class swapSetting(Enum):
    """
    Settings for the swap model
    """
    reverse = 0
    random = 1
    sectionReverse = 2
    sectionRandom = 3


@dataclass
class swap(baseModel):
    """
    Model for positional character swapping


    setting:
        Description: Setting the swap model will use
        Type       : int
        Default    : 0
        NOTE       : Can be positive and negative
    reverse_amount:
        Description: Scope of all the ascii letters it allows
        Type       : helpers.ascii_scope
        Default    : default helpers.ascii_scope
        NOTE       : -
    section_amount:
        Description: If defined, will scramble the helpers.ascii_scope for extra encryption
        Type       : helpers.scrambler
        Default    : None
        NOTE       : -
    scrambler:
        Description: Scrambler is used when swapSetting random or sectionRandom is set
        Type       : helpers.scrambler
        Default    : None
        NOTE       : If not defined when using swapSetting random or sectionRandom, a TypeError is raised.
    """
    # Vars for the inherited model class
    name: str = field(default='model.swap', init=False)
    type: typeInput = field(default=typeInput.all, init=False)

    # Model specific settings
    setting: swapSetting = field(default=swapSetting.reverse)
    reverse_amount: int = field(default=1)
    section_amount: int = field(default=1)
    scrambler: 'scrambler' = field(default=None)

    # Local variables, not exported
    __encrypt_toggle: bool = field(default=True, init=False)

    def __post_init__(self):
        """
        Function that should be used for checking the validity of the variables
        """
        if self.setting in [swapSetting.reverse, swapSetting.random] and self.section_amount != 1:
            warn("Setting the section_amount while not using a section setting will not change the output",
                 SyntaxWarning)

        if self.setting in [swapSetting.random, swapSetting.sectionRandom]:
            if self.scrambler is None:
                raise TypeError("No scrambler model has been given")

        if self.setting == swapSetting.random:
            if self.reverse_amount != 1:
                warn("swapSetting.random ignores reverse_amount and changing this will not change the output",
                     SyntaxWarning)

        if self.reverse_amount < 1:
            raise TypeError("Setting 'reverse_amount' should be at least 1")
        if self.section_amount < 1:
            raise TypeError("Setting 'section_amount' should be at least 1")

        # Update the id when the object constructor is called
        self.update_id()

    def __reverse_swap(self, data: bytearray) -> bytearray:
        """
        Internal function for reversing incoming data
        :param data: The data
        :return: The reversed data
        """
        if len(data) <= self.reverse_amount * 2 - 1:
            return data
        return data[-self.reverse_amount:] + self.__reverse_swap(
            data[self.reverse_amount:-self.reverse_amount]
        ) + data[:self.reverse_amount]

    def __scramble_swap(self, data: bytearray) -> bytearray:
        """
        Internal function for scrambling the data (setting random)
        :param data: The data
        :return: The scrambled data
        """
        if self.__encrypt_toggle:
            return self.scrambler.scramble(data)
        return self.scrambler.unscramble(data)

    def __section_swap(self, data: bytearray, function: Callable[[bytearray], bytearray]) -> bytearray:
        """
        Function for using a function over multiple sections of the given data
        :param data: The data
        :param function: Function that swaps data given to it
        :return: The section swapped data
        """
        if len(data) <= self.section_amount * 2 - 1:
            return data
        return function(data[:self.section_amount]) + self.__section_swap(data[self.section_amount:], function)

    def encrypt(self, content: bytearray) -> bytearray:
        """
        Encrypt the input that is given
        :param content: string you want encrypted
        :return: encrypted input
        """
        if self.setting == swapSetting.reverse:
            return self.__reverse_swap(content)
        elif self.setting == swapSetting.random:
            return self.__scramble_swap(content)
        elif self.setting == swapSetting.sectionReverse:
            return self.__section_swap(content, lambda x: self.__reverse_swap(x))
        elif self.setting == swapSetting.sectionRandom:
            return self.__section_swap(content, lambda x: self.__scramble_swap(x))
        raise TypeError(f'swapSetting {self.setting} is not supported')

    def decrypt(self, content: bytearray) -> bytearray:
        """
        Decrypt the input that is given
        :param content: string you want decrypted
        :return: decrypted input
        """
        self.__encrypt_toggle = False
        content = self.encrypt(content)
        self.__encrypt_toggle = True
        return content

    @staticmethod
    def __export__(model: 'swap') -> List[Any]:
        """
        Custom magic method for exporting models
        Return all the variables needed to recreate the model
        :return: List with values for init
        """
        return [
            model.setting.value,
            model.reverse_amount,
            model.section_amount,
            export_model(model.scrambler)
        ]

    @staticmethod
    def __import__(attributes: List[Any]) -> 'swap':
        return swap(
            setting=swapSetting(attributes[0]),
            reverse_amount=attributes[1],
            section_amount=attributes[2],
            scrambler=import_model(attributes[3])
        )


# Standard model variables
MAIN_MODULE = swap

