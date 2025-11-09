'''Query service module for the Text-to-SQL Chatbot with RAG application.
'''
import os
import logging

from pydantic import BaseModel

from retriever_node import retriever_node
from sql_node import sql_generator_node
from sql_validator import validate_sql, allowed_tables_from_db
from sql_executor import execute_sql

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_TABLES = allowed_tables_from_db(os.getenv("DATABASE_PATH"))


class QueryRequest(BaseModel):
    """Query request"""
    question: str
    show_sql: bool = True


def query(req: QueryRequest):
    """Process a query request through the RAG pipeline."""
    logger.info("Processing query request: %s", req.question)
    state = {"question": req.question, "messages": []}

    # 1. retrieve
    state = retriever_node(state)

    # 2. generate SQL
    state = sql_generator_node(state)
    sql = state["generated_sql"]
    ok, reason = validate_sql(sql, ALLOWED_TABLES)
    if not ok:
        logger.error("Generated SQL is not valid: %s", reason)

    # 3. execute
    cols, rows = execute_sql(sql)

    # format result rows
    result = [dict(zip(cols, r)) for r in rows]
    return {"sql": sql if req.show_sql else None, "cols": cols, "rows": result}

# print(query(QueryRequest(question="quantas vendas foram feitas em 24?")))
