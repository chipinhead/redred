import os
from langchain_postgres import PGVector
from llm.model import embedding

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_CONNECTION_STRING = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_vector_store(collection):
    return PGVector(
        collection_name=collection,
        connection=DB_CONNECTION_STRING,
        embeddings=embedding,
    )
