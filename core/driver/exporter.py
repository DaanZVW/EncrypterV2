# Library's
import os
import json
import importlib
from datetime import datetime
from dataclasses import dataclass, field, InitVar, KW_ONLY
from typing import Dict, Any, List

# Drivers
from core.driver.encoder import register_encrypter_type


@dataclass
class exporter:
    save_dir: str
    helper_dir: InitVar[str]
    model_dir: InitVar[str]

    _paths: List[str] = field(init=False, default_factory=list, repr=False)
    _model_info: Dict[str, Any] = field(init=False, default_factory=dict)
    _home_path: str = field(default=os.environ['PYTHONPATH'].split(os.pathsep)[0], init=False)
    _ = KW_ONLY
    auto_add_models: InitVar[bool] = field(default=True)
    auto_import_models: InitVar[bool] = field(default=True)

    def __post_init__(self, helper_dir: str, model_dir: str, auto_add_models: bool, auto_import_models: bool):
        if auto_add_models:
            helper_paths = self.get_all_files_from_dir(os.path.join(self._home_path, helper_dir))
            model_paths = self.get_all_files_from_dir(os.path.join(self._home_path, model_dir))
            self.add_files(*helper_paths, *model_paths)

        if auto_import_models:
            self.import_added_files()

    def get_all_files_from_dir(self, directory: str):
        root, models, _ = next(os.walk(directory))
        models = [os.path.join(root, model) for model in models if not model.endswith('__')]

        file_paths = []
        for model in models:
            for root, _, files in os.walk(model):
                if not root.endswith('__'):
                    file_paths += [os.path.join(root, file) for file in files if not file.startswith('__')]

        return file_paths

    def add_files(self, *file_path: str) -> bool:
        for file in file_path:
            if file not in self._paths:
                self._paths.append(file)
        return True

    def import_added_files(self) -> bool:
        for file_path in self._paths:
            package_name = file_path.removeprefix(self._home_path).replace(os.path.sep, '.')[1:-3]
            module = importlib.import_module(package_name)

            self._model_info[file_path] = {
                'type': module.MAIN_MODULE
            }

            register_encrypter_type(module.MAIN_MODULE, 1)
        return True

