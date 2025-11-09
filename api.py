'''api.py - FastAPI application for Text-to-SQL service'''

import logging
from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from query_service import QueryRequest as ServiceQueryRequest
from query_service import query

app = FastAPI(title="Text-to-SQL API", version="1.0.0")

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# models for request/response
class QueryRequest(BaseModel):
    '''Query request'''
    question: str
    show_sql: bool = True

class QueryResponse(BaseModel):
    '''Query response'''
    success: bool
    sql: Optional[str] = None
    cols: Optional[List[str]] = None
    rows: Optional[List[Dict]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    '''Root endpoint'''
    return {"message": "Text-to-SQL API", "docs": "/docs"}


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    '''Process a query request'''
    try:
        logger.info("Pergunta: %s", request.question)

        # Usar o query service
        service_request = ServiceQueryRequest(
            question=request.question,
            show_sql=request.show_sql
        )

        result = query(service_request)

        return QueryResponse(
            success=True,
            sql=result["sql"],
            cols=result["cols"],
            rows=result["rows"]
        )

    except (ValueError, RuntimeError, ConnectionError, KeyError) as e:
        logger.error("Erro: %s", str(e))
        return QueryResponse(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
