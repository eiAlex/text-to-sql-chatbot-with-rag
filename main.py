'''Main module for the Text-to-SQL Chatbot with RAG application.
'''
import os
import sqlite3
import hashlib
from tqdm import tqdm
from dotenv import load_dotenv
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# Load environment variables from .env file
load_dotenv()


# if __name__ == "__main__":
#

