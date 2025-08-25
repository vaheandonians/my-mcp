import json
from pathlib import Path

from my_mcp.utils.singleton_meta import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def configure(self, config_dict_or_path: dict | Path | None = None):
        if isinstance(config_dict_or_path, dict):
            config_dict = config_dict_or_path
        elif config_dict_or_path is None:
            current_dir = Path.cwd()
            config_path = None

            while current_dir != current_dir.parent:
                potential_path = current_dir / "config.json"
                if potential_path.exists():
                    config_path = potential_path
                    break
                current_dir = current_dir.parent

            if config_path is None:
                raise FileNotFoundError(
                    "Could not find config.json in any parent directory"
                )

            with open(config_path) as file:
                config_dict = json.load(file)
        else:
            with open(config_dict_or_path) as file:
                config_dict = json.load(file)
        for key, value in config_dict.items():
            self.__dict__[key] = value
        return self

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent.parent

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        raise AttributeError(f"No such attribute: {item}")
