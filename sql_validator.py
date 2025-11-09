import os
import sqlglot
import sqlite3
from typing import Tuple, Set

DISALLOWED = {"insert","update","delete","drop","alter",
            "create","replace","attach","detach","truncate","pragma","vacuum","merge"}

ALLOWED_STATEMENTS = {"select"}

def extract_tables(sql: str) -> Set[str]:
    '''Extract table names from a SQL query.'''

    try:
        parsed = sqlglot.parse_one(sql, read="sqlite")
    except Exception:
        return set()
    tables = {t.name for t in parsed.find_all(sqlglot.exp.Table)}
    return tables

def allowed_tables_from_db(sqlite_path: str):
    '''Get allowed table names from the SQLite database.'''
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [t[0] for t in cur.fetchall()]
    conn.close()
    return set(tables)

def validate_sql(sql: str, allowed_tables: Set[str]) -> Tuple[bool, str]:
    '''Validate the generated SQL query.
    Checks for disallowed keywords, only allows SELECT statements, and disallows        
    use of disallowed tables.
    '''
    if ";" in sql:
        return False, "semicolon or multiple statements not allowed"
    low = sql
    for kw in DISALLOWED:
        if f" {kw} " in f" {low} ":
            return False, f"disallowed keyword: {kw}"
    try:
        parsed = sqlglot.parse_one(sql, read="sqlite")
    except Exception as e:
        return False, f"sql parse error: {e}"
    if parsed.key.lower() not in ALLOWED_STATEMENTS:
        return False, "only SELECT statements allowed"
    tables = extract_tables(sql)
    if not tables.issubset(allowed_tables):
        return False, f"disallowed tables used: {tables - allowed_tables}"
    return True, "ok"

