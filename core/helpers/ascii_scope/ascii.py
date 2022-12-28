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
    name: str = field(default='helpers.ascii_scope', init=False)

    # Helper variables, will be exported
    setting: asciiSetting = field(default=asciiSetting.full)
    extra_scope_chars: Union[bytes, None] = field(default=b'\n\t ')

    # Local variables, will not be exported
    scope: bytearray = field(default_factory=bytearray, init=False)

    def __post_init__(self):
        # Update the id when the object constructor is called
        self.update_id()

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
            if check_func(chr(number)):
                self.scope += number.to_bytes(1, 'little')

        if self.extra_scope_chars is not None:
            self.scope += self.extra_scope_chars

    def get_index(self, char: bytes) -> Union[bool, int]:
        try:
            return self.scope.index(char)
        except ValueError:
            raise ValueError(f"Given character '{char}' does not fit the scope '{self.setting}'")

    @staticmethod
    def __export__(model: 'ascii_scope') -> List[Any]:
        return [
            model.setting.value,
            model.extra_scope_chars.decode('utf-8')
        ]

    @staticmethod
    def __import__(attributes: Any) -> 'ascii_scope':
        return ascii_scope(
            setting=asciiSetting(attributes[0]),
            extra_scope_chars=attributes[1].encode('utf-8')
        )


# Standard model variables
MAIN_MODULE = ascii_scope
MODULE_ATTRIBUTES = [asciiSetting, list]

