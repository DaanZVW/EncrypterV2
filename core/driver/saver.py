import os
from typing import Optional, Union
from dataclasses import dataclass, field


@dataclass
class saver:
    home_path: str = field(default=None)
    save_dir: str = field(default=None)

    def __post_init__(self):
        if self.home_path is None:
            self.home_path = os.environ['PYTHONPATH'].split(os.pathsep)[0]

        if self.save_dir is None:
            self.save_dir = 'saves'

        if not os.path.isdir((save_path := os.path.join(self.home_path, self.save_dir))):
            os.mkdir(save_path)

    def write(self, filename: str, content: str, absolute: Optional[bool] = False,
              overwrite: Optional[bool] = False) -> bool:
        if type(content) is not str:
            return False

        if not absolute:
            filename = os.path.join(self.home_path, self.save_dir, filename)

        if not overwrite:
            if os.path.isfile(filename):
                return False

        with open(filename, 'w') as file:
            file.write(content)

        return True

    def read(self, filename: str, absolute: Optional[bool] = False) -> Union[bool, str]:
        if not absolute:
            filename = os.path.join(self.home_path, self.save_dir, filename)

        if not os.path.isfile(filename):
            return False

        with open(filename, 'r') as file:
            return file.read()


