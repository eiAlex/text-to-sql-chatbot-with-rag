'''
    Retriever module for the Text-to-SQL Chatbot with RAG application.
'''
import logging
import os
from typing import List, TypedDict

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)


class RAGState(TypedDict, total=False):
    """State for the RAG loop."""
    question: str
    retrieved_docs: List[str]
    generated_sql: str
    validated_sql: str
    sql_result: List[dict]
    messages: List[dict]


embeddings = HuggingFaceEmbeddings(model_name=os.getenv("EMBED_MODEL"))
vectordb = Chroma(persist_directory=os.getenv("VECTOR_STORE_DIR"),
                embedding_function=embeddings, collection_name=os.getenv("VECTOR_COLLECTION"))


# Increments the number of documents retrieved for reranking,
# to allow the rerank model to choose the best ones
initial_k = int(os.getenv("TOP_K")) * 3
retriever = vectordb.as_retriever(search_kwargs={"k": initial_k})

# Initialize the rerank model
rerank_model = CrossEncoder(os.getenv("RERANK_MODEL"))


def rerank_documents(question: str, docs: List, top_k: int = None) -> List:
    """
    Re-ranks documents using a CrossEncoder model.
    Args:
        question: The user's question
        docs: List of retrieved documents
        top_k: Number of documents to return (default: TOP_K from .env)
    Returns:
        List of re-ranked documents
    """
    if not docs:
        return []

    if top_k is None:
        top_k = int(os.getenv("TOP_K", "5"))

    pairs = [(question, doc.page_content) for doc in docs]

    # Calc the estimated scores
    scores = rerank_model.predict(pairs)
    # make a combined list of docs and scores
    doc_scores = list(zip(docs, scores))
    doc_scores.sort(key=lambda x: x[1], reverse=True)

    # return the top_k documents
    reranked_docs = [doc for doc, _ in doc_scores[:top_k]]
    logging.info("Reranked %s documents, returning top %s", len(docs), len(reranked_docs))
    return reranked_docs


def retriever_node(state: RAGState) -> RAGState:
    """
    Retrieves documents based on the given state.
    Args:
        state (RAGState): The state 
        containing the question.

    Returns:
        RAGState: The updated state with retrieved documents.
    """
    # Retrieve initial documents
    docs = retriever.invoke(state["question"])

    # Rerank the retrieved documents
    reranked_docs = rerank_documents(state["question"], docs)

    state["retrieved_docs"] = [d.page_content for d in reranked_docs]
    print(len(state["retrieved_docs"]))
    return state


# print(retriever_node({"question": "Comércio ABC S/A"}))
