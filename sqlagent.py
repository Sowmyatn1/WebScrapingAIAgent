from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

def ask_agent(query):
    
    db = SQLDatabase.from_uri("sqlite:///doctors.db")

    toolkit = SQLDatabaseToolkit(db=db, llm=ChatOpenAI(temperature=0))

    agent = create_sql_agent(
        llm=ChatOpenAI(temperature=0),
        toolkit=toolkit,
        verbose=True,
        handle_parsing_errors=True 
    )

    #query = "is doctor Dr B. L. Avinash  available on 2025-10-15 at 1:00 PM?"
    sql_result = agent.run(query)

    reasoning_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    prompt = f"""
    You are a medical scheduling assistant that queries a database to answer questions about doctor availability.

    - The database has two main tables:
    1. doctor(doctor_id, name, specialization, qualification, experience, consultation_fee, location)
    2. availability(id, doctor_id, date, available_slots)

    - The availability table stores all appointment times for doctors, linked by doctor_id.

    Given the query {query} :
    the result for the question is in  {sql_result}
    
    Answer the question asked in the query:
      When a question asks about:
    - availability or appointment times → query the availability table (JOIN with doctor)
    - doctor details (qualification, fee, etc.) → query the doctor table
    - specific date or time → filter by availability.date and/or available_slots
    - If the result is empty or None, respond:
    - "Sorry, there are no available appointments for this doctor right now."

Answer in one line if possible.
    Always return the **next available date and time** for appointment-related questions.

    General Instructions
    - If the result provides a clear answer, respond with a concise factual response.
    - If the question can be answered as Yes/No, respond simply with "Yes" or "No".
    - Only include an explanation if it helps clarify how the result answers the question.
    - Do not invent or assume data not present in the SQL result.
    """

    messages = [
                SystemMessage(content="you are an expert in analyzing sql results analyse the sql results from the sql agent and answer the question asked in the query"),
                HumanMessage(content=prompt)
            ]


    final_response = reasoning_llm.invoke(messages)
    print(final_response.content.strip())
    return final_response.content.strip()
