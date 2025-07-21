from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser

from app.agent.client import get_model
from app.agent.tools.vector_tool import vector_tool


def unicatt_assistant(user_input: str) -> str:
    """
    This function invokes an AI assistant that answers user questions
    about the latest news published on the official Università Cattolica website.
    It uses a vector search tool to retrieve relevant information.

    Args:
        user_input (str): The user's natural language question.

    Returns:
        str: The assistant's answer.
    """

    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant designed to answer user questions "
        "based on the latest news published on the official website of "
        "Università Cattolica del Sacro Cuore (https://www.unicatt.it/). "
        "Use the data retrieved from the vector database to respond accurately and informatively. "
        "If there is not enough information in the database, politely say so. "
        "Always respond in a professional and clear tone."
    )

    llm = get_model()

    chain: Runnable = prompt | llm.bind_tools([vector_tool]) | StrOutputParser()

    response = chain.invoke({"input": user_input})
    return response

