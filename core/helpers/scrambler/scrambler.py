# Library's
import time
import random
from enum import Enum
from typing import List, Any
from dataclasses import dataclass, field

# Drivers
from core.driver.basemodel import baseHelper


class scrambleSetting(Enum):
    customSeed = 0
    randomSeed = 1


@dataclass
class scrambler(baseHelper):
    # Vars for the inherited model class
    name: str = field(default='helper.scrambler', init=False)

    setting: scrambleSetting = field(default=scrambleSetting.randomSeed)
    seed: int = field(default=0)

    def __post_init__(self):
        # Update the id when the object constructor is called
        self.update_id()

        if self.setting == scrambleSetting.randomSeed:
            self.seed = time.time_ns()

    def scramble(self, unscrambled_list: List[Any]) -> List[Any]:
        random.seed(self.seed)
        random.shuffle(unscrambled_list)
        return unscrambled_list

    def unscramble(self, scrambled_list: List[Any]) -> List[Any]:
        range_list = list(range(len(scrambled_list)))
        shuffled_data = list(zip(scrambled_list, self.scramble(range_list)))
        shuffled_data.sort(key=lambda x: x[1])
        return list(map(lambda x: x[0], shuffled_data))

    def __export__(self) -> List[Any]:
        """Magic method for exporting"""
        return [
            scrambleSetting.customSeed.value,
            self.seed
        ]


# Standard model variables
MAIN_MODULE = scrambler
MODULE_ATTRIBUTES = [scrambleSetting, int]
