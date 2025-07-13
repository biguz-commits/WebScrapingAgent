### Fallo funzionare in un grafo langgraph
### Aggiungi migrazioni per gestire la logica del db
### Aggiungi un job che aggiorna il db ogni tot leggedno i contenuti della homepage unicatt
### Rendi i contenuti vettori, così da avere una generazione della risposta molto migliore
### Crea la UI con typescript



from typing import TypedDict
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

from dotenv import load_dotenv
from typing_extensions import Annotated

from app.agent.client import get_model
from app.agent.prompt import get_prompt
from app.db.DbConnection import DbConnection


load_dotenv()

llm = get_model()
query_prompt_template = get_prompt()

db = DbConnection()
db = db.langchain_db()


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(question:str):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": question,
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}


def execute_query(query: str):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(query)}

def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}