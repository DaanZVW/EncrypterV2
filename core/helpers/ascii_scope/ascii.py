# Library's
from enum import Enum
from typing import List, Any, Union
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseHelper


class asciiSetting(Enum):
    """
    Different types of settings for the ascii scope class
    """
    full = [1, 255]
    lettersDigits = [48, 122]
    lettersAll = [65, 122]
    lettersLower = [97, 122]
    lettersHigher = [65, 90]
    printable = [33, 255]
    test = [97, 102]


@dataclass
class ascii_scope(baseHelper):
    # Vars for the inherited model class
    name: str = field(default='ascii_scope', init=False)

    # Setting which the model follows
    setting: asciiSetting = field(default=asciiSetting.full)
    # Characters it will include in scope (must be within 8-bit ascii_scope)
    extra_scope_chars: Union[None, List[str]] = field(default_factory=lambda: ['\n', '\t', ' '])

    scope: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        if self.setting in (asciiSetting.lettersAll, asciiSetting.lettersLower, asciiSetting.lettersHigher):
            def check_func(char):
                return char.isalpha()
        elif self.setting is asciiSetting.lettersDigits:
            def check_func(char):
                return char.isalnum()
        elif self.setting is asciiSetting.printable:
            def check_func(char):
                return char.isprintable()
        else:
            def check_func(_):
                return True

        start, stop = self.setting.value
        for number in range(start, stop + 1):
            if check_func((character := chr(number))):
                self.scope += character

        if self.extra_scope_chars is not None:
            self.scope += self.extra_scope_chars

    def getIndex(self, char: str) -> Union[bool, int]:
        try:
            return self.scope.index(char)
        except ValueError:
            raise ValueError(f"Given character '{char}' does not fit the scope '{self.setting}'")

    def __export__(self) -> List[Any]:
        return [
            self.setting.value,
            self.extra_scope_chars
        ]

    def __len__(self):
        return len(self.scope)


# Standard model variables
MAIN_MODULE = ascii_scope
MODULE_ATTRIBUTES = [asciiSetting, list]

