from storage.db import DB_CONNECTION_STRING
from sqlalchemy import create_engine, text

engine = create_engine(DB_CONNECTION_STRING)

with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS langchain_pg_embedding;"))
    connection.execute(text("DROP TABLE IF EXISTS langchain_pg_collection;"))
    connection.execute(text("DROP TABLE IF EXISTS reddit_content;"))
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
