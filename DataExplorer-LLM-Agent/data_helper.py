# Packages
import pandas as pd

from langchain_experimental.agents.agent_toolkits.pandas.base import(
    create_pandas_dataframe_agent
)
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from pydantic.v1 import BaseModel

load_dotenv()
# Api-key
my_key_openai = os.getenv("openai_apikey")

# LLMs
llm_gpt = ChatOpenAI(api_key=my_key_openai, model='gpt-4o', temperature=0)
selected_llm = llm_gpt


# Summarize data
def summarize_data(data_file):
    df = pd.read_csv(data_file, low_memory=False)
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True,allow_dangerous_code=True,
    agent_executor_kwargs={'handle_parsing_errors': True})
    data_summary = {}

    data_summary['initial_data_sample'] = df.head()
    data_summary['column_descriptions'] = pandas_agent.run('Make a table with the columns in the data. The table should contain the names of the columns and a brief description of the information they contain. Export this as a table')
    data_summary['missing_values'] = pandas_agent.run("Is there missing data in this dataset? If so, how many? Answer 'There is missing data in X number of cells in this dataset.'")
    data_summary['duplicate_values'] = pandas_agent.run("Is there duplicate data in this dataset? If so, how many? Answer 'There is duplicate data in X number of cells in this dataset.'")
    data_summary['essential_metrics'] = df.describe()

    return data_summary

# get dataframe
def get_dataframe(data_file):
    df = pd.read_csv(data_file, low_memory=False)
    return df


# Analyze trend
def analyze_trend(data_file, variable_of_interest):
    df = pd.read_csv(data_file, low_memory=False)
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, allow_dangerous_code=True, agent_executor_kwargs={"handle_parsing_errors":"True"})
    trend_response = pandas_agent.run(f"Briefly interpret the trend of change of the following variable in the data set: {variable_of_interest} Dont refusal to interpret. Since the rows in the data are date-based from past to present, you can comment by looking at the rows in the data")
    return trend_response


# ask question
def ask_question(data_file, question):
    df = pd.read_csv(data_file, low_memory=False)
    pandas_agent = create_pandas_dataframe_agent(selected_llm, df, verbose=True, allow_dangerous_code=True, agent_executor_kwargs={"handle_parsing_errors":"True"})
    AI_Response = pandas_agent.run(question)
    return AI_Response

