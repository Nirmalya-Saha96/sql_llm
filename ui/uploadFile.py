import os
import pandas as pd
from typing import List
from sqlalchemy import create_engine
from configs.config import Config

APP_CONFIG = Config()

class UploadFile:
    @staticmethod
    def run_pipeline(files_dir: List, chatbot: List, chatbot_functionality: str):
        if chatbot_functionality == "Process files":
            db_path = f"sqlite:///{APP_CONFIG.uploaded_files_sqldb_directory}"
            engine = create_engine(db_path)

            for file_dir in files_dir:
                file_names_with_extensions = os.path.basename(file_dir)
                file_name, file_extension = os.path.splitext(file_names_with_extensions)

                if file_extension == ".csv":
                    df = pd.read_csv(file_dir)
                elif file_extension == ".xlsx":
                    df = pd.read_excel(file_dir)
                else:
                    raise ValueError("The selected file type is not supported")
                
                df.to_sql(file_name, engine, index=False)

            print("-------------Done------------")
            chatbot.append((" ", "Uploaded files are ready. Please enter your prompt."))

            return "", chatbot
        else:
            pass
