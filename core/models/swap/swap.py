# Library's
from enum import Enum
from warnings import warn
from typing import List, Callable, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseModel, typeInput, export_model

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
    # Vars for the inherited model class
    name: str = field(default='model.swap', init=False)
    type: typeInput = field(default=typeInput.all, init=False)

    # Model specific settings
    setting: swapSetting = field(default=swapSetting.reverse)
    reverse_amount: int = field(default=1)
    section_amount: int = field(default=1)
    scrambler: 'scrambler' = field(default=None)

    # Internal variables, are not exported
    __encrypt_toggle: bool = field(default=True, init=False)

    def __post_init__(self):
        # Update the id when the object constructor is called
        self.update_id()

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

    def __reverseSwap(self, data: List[str]) -> List[str]:
        if len(data) <= self.reverse_amount * 2 - 1:
            return data
        return data[-self.reverse_amount:] + self.__reverseSwap(
            data[self.reverse_amount:-self.reverse_amount]
        ) + data[:self.reverse_amount]

    def __scrambleSwap(self, data: List[str]) -> List[str]:
        if self.__encrypt_toggle:
            return self.scrambler.scramble(data)
        return self.scrambler.unscramble(data)

    def __sectionSwap(self, data: List[str], function: Callable[[List[str]], List[str]]) -> List[str]:
        if len(data) <= self.section_amount * 2 - 1:
            return data
        return function(data[:self.section_amount]) + self.__sectionSwap(data[self.section_amount:], function)

    def encrypt(self, content: str) -> str:
        content = list(content)
        if self.setting == swapSetting.reverse:
            content = self.__reverseSwap(content)
        elif self.setting == swapSetting.random:
            content = self.__scrambleSwap(content)
        elif self.setting == swapSetting.sectionReverse:
            content = self.__sectionSwap(content, lambda x: self.__reverseSwap(x))
        elif self.setting == swapSetting.sectionRandom:
            content = self.__sectionSwap(content, lambda x: self.__scrambleSwap(x))
        return "".join(content)

    def decrypt(self, content: str) -> str:
        self.__encrypt_toggle = False
        content = self.encrypt(content)
        self.__encrypt_toggle = True
        return content

    def __export__(self) -> List[Any]:
        return [
            self.setting.value,
            self.reverse_amount,
            self.section_amount,
            export_model(self.scrambler)
        ]


# Standard model variables
MAIN_MODULE = swap
MODULE_ATTRIBUTES = [swapSetting, int, int, scrambler]

