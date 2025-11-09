'''SQL execution utility functions.'''
import sqlite3
import re
import os
from typing import Tuple, List, Any



def open_ro_conn():
    '''Open a read-only connection to the SQLite database.'''
    return sqlite3.connect(f"file:{os.getenv('DATABASE_PATH')}?mode=ro", uri=True, check_same_thread=False)

def enforce_limit(sql: str, limit: int = 1000) -> str:
    '''Ensure the SQL query has a LIMIT clause.'''
    if re.search(r'\blimit\b', sql, re.I):
        return sql
    return f"{sql} LIMIT {limit}"

def execute_sql(sql: str, row_limit: int = 1000, timeout=5.0) -> Tuple[List[str], List[Tuple[Any]]]:
    '''Execute the given SQL query with a row limit and timeout.'''

    sql = enforce_limit(sql, row_limit)
    conn = open_ro_conn()
    conn.execute(f"PRAGMA busy_timeout = {int(timeout*1000)};")
    cur = conn.cursor()
    cur.execute(sql)
    cols = [c[0] for c in cur.description] if cur.description else []
    rows = cur.fetchmany(row_limit)
    conn.close()
    return cols, rows