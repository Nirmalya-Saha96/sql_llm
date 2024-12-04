
import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil

print("Environment variables are loaded:", load_dotenv())


class Config:
    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config=app_config)
        self.remove_directory(self.uploaded_files_sqldb_directory)

    def load_directories(self, app_config):
        self.stored_csv_xlsx_directory = here(app_config["directories"]["stored_csv_xlsx_directory"])
        self.sqldb_directory = str(here(app_config["directories"]["sqldb_directory"]))
        self.uploaded_files_sqldb_directory = str(here(app_config["directories"]["uploaded_files_sqldb_directory"]))
        self.stored_csv_xlsx_sqldb_directory = str(here(app_config["directories"]["stored_csv_xlsx_sqldb_directory"]))
        self.persist_directory = app_config["directories"]["persist_directory"]

    def remove_directory(self, directory_path: str):
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory_path}' does not exist.")
