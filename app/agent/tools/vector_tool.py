from typing import Optional, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from langchain_core.tools import tool

from pydantic import BaseModel, Field

from app.agent.Embeddings import Embeddings
from app.db.DbConnection import DbConnection


class VectorInput(BaseModel):
    query: Optional[str] = Field(description="Query given by the user that needs to be "
                                             "embedded and searched in the database.")

@tool(args_schema=VectorInput, response_format="content_and_artifact")
def vector_tool(query: str):
    """
    This tool is intended to query a vector database and retrieve
    the most similar vector with respective metadadata.
    """
    output_prompt = ("This is what we have in the database, please use these "
                     "data to answer to the user.")
    db = DbConnection()
    embeddings = Embeddings()
    results = embeddings.lookup(db=Annotated[Session, Depends(db.create_session)],
                      query=query
                      )
    return f"{output_prompt}\n", {"results": results}






