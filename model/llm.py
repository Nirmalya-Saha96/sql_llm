import os
from typing import List, Tuple
from configs.config import Config
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.llms import Ollama
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
import langchain

langchain.debug = True
APP_CONFIG = Config()
llm = Ollama(model="llama3.2")

class LlmModel:
    @staticmethod
    def respond(chatbot: List, message: str, app_functionality: str) -> Tuple:
        if app_functionality == "Chat":
            if os.path.exists(APP_CONFIG.uploaded_files_sqldb_directory):
                engine = create_engine(
                    f"sqlite:///{APP_CONFIG.uploaded_files_sqldb_directory}")
                db = SQLDatabase(engine=engine)
            else:
                chatbot.append(
                    (message, f"SQL DB from the uploaded csv/xlsx files does not exist. Please first upload the csv files from the chatbot."))
                return "", chatbot, None
            
            print(db.dialect)
            print(db.get_usable_table_names())
            
            agent_executor = create_sql_agent(
                llm=llm,
                db=db,
                verbose=True,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            )
            
            response = agent_executor.invoke({"input": message})
            response = response["output"]

            chatbot.append((message, response))

            return "", chatbot
        else:
            pass
