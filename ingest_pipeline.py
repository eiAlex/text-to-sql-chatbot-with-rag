'''Main module for the Text-to-SQL Chatbot with RAG application.
'''
import os
import sqlite3
import hashlib
import logging
import torch


from tqdm import tqdm
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load environment variables from .env file first
load_dotenv()
logging.basicConfig(level=logging.INFO)


# Initialize HuggingFaceEmbeddings
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logging.info("Using device: %s", DEVICE)

model = HuggingFaceEmbeddings(model_name=os.getenv("EMBED_MODEL"), model_kwargs={"device": DEVICE})


vectorstore = Chroma(
    collection_name=os.getenv("VECTOR_COLLECTION"),
    embedding_function=model,
    persist_directory=os.getenv("VECTOR_STORE_DIR")
)

logging.info("Embedding function initialized.")

def row_hash(values):
    """Generate unique hash for a row."""
    return hashlib.sha256("|".join(map(str, values)).encode()).hexdigest()

def row_to_text(table, cols, row):
    """Convert SQLite row into a readable text chunk."""
    return f"Table: {table}\n" + "\n".join([f"{c}: {v}" for c, v in zip(cols, row)])

def index_table(conn, table):
    """Index a single table into the vector store."""
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_xinfo({table});")
    cols = [c[1] for c in cur.fetchall()]
    cur.execute(f"SELECT {', '.join(cols)} FROM {table}")
    rows = cur.fetchall()

    docs, ids, metas = [], [], []
    for r in rows:
        txt = row_to_text(table, cols, r)
        pk = str(r[0])
        hid = row_hash(r)
        ids.append(f"{table}:{pk}")
        docs.append(txt)
        metas.append({"table": table, "pk": pk, "hash": hid})

    # Add to Chroma vector store
    vectorstore.add_texts(texts=docs, metadatas=metas, ids=ids)

def main():
    """Main indexing pipeline."""
    logging.info("index_tables: Starting indexing process.")

    conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")

    # Get table names
    tables = [t[0] for t in cur.fetchall()]
    logging.info("Indexing %d tables.", len(tables))

    for table in tqdm(tables, desc="Indexing tables"):
        index_table(conn, table)

    conn.close()
    logging.info("Indexing complete and persisted in Chroma.")

if __name__ == "__main__":
    main()
    logging.info("index_tables: Exiting.")
