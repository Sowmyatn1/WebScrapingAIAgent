#from langchain.chat_models import ChatOpenAI
#from langchain.sql_database import SQLDatabase
from langchain_community.utilities import SQLDatabase
#from langchain.agents import create_sql_agent
#from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits import SQLDatabaseToolkit
#from langchain.chat_models import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import os
#from langchain.agents import create_agent
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from dotenv import load_dotenv


def ask_agent(query):
    load_dotenv()

    llm = init_chat_model(
        model="gpt-4o-mini",      
        model_provider="openai",
        temperature=0.3)

    db = SQLDatabase.from_uri("sqlite:///doctors.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    tools = toolkit.get_tools()


    system_prompt = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    Then you should query the schema of the most relevant tables.
    """.format(
        dialect=db.dialect,
        top_k=5,
    )



    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True,
        system_prompt=system_prompt
    )

    # Your question
    question = "is dr pankaj available on 2025-10-15 at 1:00 PM?"

    response = agent({"input": question})

    # Print the final answer
    print(response)

    return response
