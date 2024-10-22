from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy import text  # Import text for executing raw SQL
from pgvector.sqlalchemy import Vector
from config.db import DB_CONNECTION_STRING

# Define the base for your models
Base = declarative_base()

# Define your Content model
class RedditContent(Base):
    __tablename__ = 'reddit_content'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(255), nullable=False)
    chunk_id = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(Text, nullable=True)
    body = Column(Text, nullable=False)
    subreddit = Column(String(255), nullable=False)
    permalink = Column(Text, nullable=False)
    url = Column(Text, nullable=True)
    parent_id = Column(String(255), nullable=True)
    created = Column(TIMESTAMP, nullable=False)
    ups = Column(Integer, nullable=True)
    downs = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    embedding = Column(Vector(1536), nullable=True)  # Embedding vector

# Connect to the database
engine = create_engine(DB_CONNECTION_STRING)

# Explicit transaction block to create the extension
with engine.begin() as connection:  # This automatically commits or rolls back
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

# Create tables that do not exist
Base.metadata.create_all(engine)