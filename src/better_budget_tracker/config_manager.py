import os
import json
from dataclasses import dataclass
from enum import Enum

class MissingFile(Enum):
    DATA_DIR = 1
    CONFIG_FILE = 2
    REPORTS_DIR = 3
    DB_FILE = 4

@dataclass
class Config:
    """
    Dataclass for the config

    Attributes:
        data_dir: The absolute path to the data directory.
        data_dir: The absolute path to the database file.
        data_dir: The absolute path to the reports directory.
    """
    data_dir: str
    db_file: str
    reports_dir: str


class ConfigManager:
    """
    A class to manage the config and directories where data is stored.
    """
    def __init__(self) -> None:
        self.config_dir = os.path.expanduser("~/.better_budget_tracker")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.config_log = ""
        self._defaults = {
            "data_dir": os.path.join(self.config_dir,"data"),
            "db_file": "budget_data.db",
            "reports_dir": os.path.join(self.config_dir,"reports"),
        }

        self.exists_config_dir()
        self.exists_config_file()
        self.config = self.load_config()

        self.exists_report_dir()
        self.exists_data_dir()
        self.exists_db_file()

        self.config_log += self.display_config()

    def display_config(self) -> str:
        return "\n".join(
            [f"Using {self.config.reports_dir}",
             f"Using {self.config.data_dir}",
             f"Using {self.config.db_file}"]
        )

    def exists_config_dir(self):
        """
        Checks if the config directory exists. If not, creates it.
        """
        if not os.path.isdir(self.config_dir):
            os.makedirs(self.config_dir)
            self.config_log += f"Created config path at {self.config_dir}\n"
        else:
            self.config_log += f"Using config path {self.config_dir}\n"

    def exists_config_file(self):
        """
        Checks if the config file exists. If not, create it with defaults.
        """
        if not os.path.isfile(self.config_file):
            with open(self.config_file, "w") as f:
                f.write(json.dumps(self._defaults))
            self.config_log += f"Created config file with defaults at {self.config_file}\n"

    def exists_report_dir(self):
        """
        Checks if the reports directory exists. If not, create it at the config location
        """
        if not os.path.isdir(self.config.reports_dir):
            os.makedirs(self.config.reports_dir)
            self.config_log += f"Created report dir at {self.config.reports_dir}\n"

    def exists_data_dir(self):
        """
        Checks if the data directory exists. If not, create it at the config location
        """
        if not os.path.isdir(self.config.data_dir):
            os.makedirs(self.config.data_dir)
            self.config_log += f"Created data dir at {self.config.data_dir}\n"

    def exists_db_file(self):
        """
        Checks if the data file exists. If not, create it at the config location
        """
        if not os.path.isfile(self.config.db_file):
            with open(self.config.db_file, "w") as f:
                self.config_log += f"Created database file at {self.config.db_file}\n"
                pass

    def load_config(self) -> Config:
        """
        Loads config from file and returns it in the Config class.

        Raises:
            FileNotFoundError: If config file does not exist.
        """
        if not os.path.isfile(self.config_file):
            raise FileNotFoundError(MissingFile.CONFIG_FILE)
        with open(self.config_file, "r") as f:
            config = json.loads(f.read())
            self.config_log += f"Loaded config file at {self.config_file}\n"
            return Config(
                data_dir=config["data_dir"],
                db_file=config["data_dir"]+"/"+config["db_file"],
                reports_dir=config["reports_dir"],
            )

#TODO: Create menu in advanced options to edit the config.