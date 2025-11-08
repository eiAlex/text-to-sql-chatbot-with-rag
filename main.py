'''Main module for the Text-to-SQL Chatbot with RAG application.
'''
import os
import torch
import sqlite3
import hashlib
from tqdm import tqdm
import logging
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# Load environment variables from .env file
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