# Library's
import time
import random
from enum import Enum
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseHelper


class scrambleSetting(Enum):
    """
    Setting for the scrambler helper
    """
    customSeed = 0
    randomSeed = 1


@dataclass
class scrambler(baseHelper):
    """
    Helper for scrambling given characters


    shift_amount:
        Description: How many shifts a char will be encrypted with
        Type       : int
        Default    : 0
        NOTE       : Can be positive and negative
    """
    # Vars for the inherited model class
    name: str = field(default='helper.scrambler', init=False)

    # Helper variables, will be exported
    setting: scrambleSetting = field(default=scrambleSetting.randomSeed)
    seed: int = field(default=0)

    def __post_init__(self):
        # Update the id when the object constructor is called
        self.update_id()

        if self.setting == scrambleSetting.randomSeed:
            self.seed = time.time_ns()

    def scramble(self, unscrambled_array: bytearray) -> bytearray:
        """
        Scramble a given bytearray. This will also scramble the given array!
        :param unscrambled_array: bytearray that needs scrambling
        :return: scrambled bytearray
        """
        random.seed(self.seed)
        random.shuffle(unscrambled_array)
        return unscrambled_array

    def unscramble(self, scrambled_array: bytearray) -> bytearray:
        """
        Unscramble a given bytearray. This will return a different array!
        :param scrambled_array: bytearray that needs unscrambling
        :return: unscrambled bytearray
        """
        range_list = bytearray(range(len(scrambled_array)))
        shuffled_data = sorted(
            zip(scrambled_array, self.scramble(range_list)),
            key=lambda x: x[1]
        )
        return bytearray(item[0] for item in shuffled_data)

    def __export__(self) -> List[Any]:
        """Magic method for exporting"""
        return [
            scrambleSetting.customSeed.value,
            self.seed
        ]


# Standard model variables
MAIN_MODULE = scrambler
MODULE_ATTRIBUTES = [scrambleSetting, int]
