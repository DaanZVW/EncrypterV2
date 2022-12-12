# Library's
import os
import json
import importlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List

# Drivers
from core.driver.encrypter import encrypter
from core.driver.basemodel import base
from core.driver.saver import saver


@dataclass
class exporter:
    save_dir: str = field(default=None)
    model_files: Dict[str, Any] = field(default_factory=dict, init=False)
    save_helper: saver = field(default_factory=saver, init=False)

    def __post_init__(self):
        home_path = os.environ['PYTHONPATH'].split(os.pathsep)[0]

        self.addFiles(
            os.path.join(home_path, 'core', 'models'), home_path
        )
        self.addFiles(
            os.path.join(home_path, 'core', 'helpers'), home_path
        )

    def addFiles(self, dir_path: str, home_path: str) -> None:
        model_files = self.getFiles(dir_path)

        for dir_path in model_files.keys():
            # Get relative python import
            py_dir_path = dir_path.removeprefix(home_path).replace(os.path.sep, '.')[1:]

            for filename in model_files[dir_path]:
                file_content = importlib.import_module(py_dir_path + '.' + filename.split('.')[0])
                try:
                    moduleID: str = file_content.MAIN_MODULE().id
                    self.model_files[moduleID] = file_content
                except AttributeError:
                    print(f"File "
                          f"'{dir_path.removeprefix(home_path)[1:]}"
                          f"{os.path.sep}"
                          f"{filename}'"
                          f" cannot be imported")

    @staticmethod
    def getFiles(dirname: str) -> Dict[str, List[str]]:
        all_files = dict()

        root, models, _ = next(os.walk(dirname))
        models = [os.path.join(root, model) for model in models]

        for model in models:
            if model.endswith('__'):
                continue

            _, _, files = next(os.walk(model))
            all_files[model] = [file for file in files if not file.startswith('__')]

        return all_files

    def exportEncrypter(self, encrypt: encrypter, filename: str, overwrite: bool = False) -> bool:
        if not isinstance(encrypt, encrypter):
            return False

        if not filename.endswith('.json'):
            filename += '.json'

        model_data = {
            'create_date': datetime.now().isoformat(),
            'models': encrypt.__export__()
        }
        model_data = json.dumps(model_data, indent=2)

        return self.save_helper.write(filename, model_data, overwrite=overwrite)

    def importEncrypter(self, filename: str) -> encrypter:
        def getAttributes(converters: List[Any], values: List[Any]):
            attrs = []
            for convert, value in zip(converters, values):
                if value is None:
                    attrs.append(None)
                elif issubclass(convert, base):
                    if isinstance(value, list) and not isinstance(convert, list):
                        attrs_other: List[Any] = getAttributes(
                            [convert for _ in range(len(value))],
                            value
                        )
                        attrs.append(attrs_other)
                    else:
                        attrs_other: List[Any] = getAttributes(
                            self.model_files[value.get('id')].MODULE_ATTRIBUTES,
                            value.get('attributes')
                        )
                        attrs.append(convert(*attrs_other))

                else:
                    attrs.append(convert(value))

            return attrs

        if not filename.endswith('.json'):
            filename += '.json'

        file_data: str = self.save_helper.read(filename)
        file_data: Dict[str, Any] = json.loads(file_data)

        encrypt = encrypter()
        model_info: List[Dict[str, Any]] = file_data.get('models')
        for model in model_info:
            module = self.model_files[model.get('id')]

            attributes = getAttributes(module.MODULE_ATTRIBUTES, model.get('attributes'))
            initialised_model = module.MAIN_MODULE(*attributes)

            encrypt.addModel(initialised_model)
        return encrypt


