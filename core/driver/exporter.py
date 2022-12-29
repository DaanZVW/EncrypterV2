# Library's
import os
import json
import importlib
from typing import List
from datetime import datetime
from dataclasses import field, InitVar, KW_ONLY

# Drivers
from core.driver.encoder import *
from core.driver.exception import *
from core.driver.basemodel import base
from core.driver.encrypter import encrypter


def file_valid(path: Union[str, None]) -> bool:
    if path is None:
        raise FileError(path, 'None provided')
    elif not os.path.isfile(path):
        raise FileError(path, 'Not found')
    return True


@dataclass
class exporter:
    save_dir: str
    helper_dir: InitVar[str]
    model_dir: InitVar[str]

    file: str = field(default=None, init=False)

    _paths: List[str] = field(init=False, default_factory=list, repr=False)
    _model_info: Dict[str, Any] = field(init=False, default_factory=dict)
    _home_path: str = field(init=False, default=os.environ['PYTHONPATH'].split(os.pathsep)[0])
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

            try:
                module = importlib.import_module(package_name)
            except SyntaxError:
                print(f"File '{file_path}' can't be imported ")
            else:
                try:
                    module_type: Type[base] = module.MAIN_MODULE
                except AttributeError:
                    print(f"File '{file_path}' can't be imported!")
                else:
                    self._model_info[file_path] = {
                        'type': module_type
                    }

                    register_encrypter_type(module_type, 1)
        return True

    def set_file_path(self, path: Union[str, None]) -> bool:
        self.file = path

        try:
            file_valid(path)
        except FileError:
            try:
                path = os.path.join(self._home_path, path)
                self.file = path
                file_valid(path)
            except FileError:
                return False
        return True

    def get_file_path(self) -> str:
        return self.file

    def export_encrypter(self, obj: encrypter) -> bool:
        try:
            file_valid(self.file)
        except FileError:
            with open(self.file, 'wb'):
                os.utime(self.file, None)

        serializable_model = [export_model(model) for model in obj.models]

        export = {
            'date': datetime.now().isoformat(),
            'models': serializable_model
        }

        with open(self.file, 'w') as f:
            json.dump(export, f, indent=2)
        return True

    def import_encrypter(self) -> encrypter:
        file_valid(self.file)

        with open(self.file, 'r') as f:
            serializable_model = json.load(f)

        with raise_error(KeyError, FileError(self.file, 'Is not an encrypter file')):
            models = serializable_model['models']

        obj = encrypter()
        for model in models:
            obj.addModel(import_model(model))
        return obj



