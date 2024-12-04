import os
import pandas as pd
from sqlalchemy import create_engine
from configs.config import Config

APP_CONFIG = Config()

if __name__ == "__main__":
    file_dir_list = os.listdir(APP_CONFIG.stored_csv_xlsx_directory)
    engine = create_engine(f"sqlite:///{APP_CONFIG.stored_csv_xlsx_sqldb_directory}")

    for file in file_dir_list:
        full_file_path = os.path.join(APP_CONFIG.stored_csv_xlsx_directory, file)
        file_name, file_extension = os.path.splitext(file)
        if file_extension == ".csv":
            df = pd.read_csv(full_file_path)
        elif file_extension == ".xlsx":
            df = pd.read_excel(full_file_path)
        else:
            raise ValueError("The selected file type is not supported")
        df.to_sql(file_name, engine, index=False)
        print("--------------Done------------------")
