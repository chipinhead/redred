from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import psycopg2
import os
from config.db import DB_CONNECTION_STRING

OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

embedding_model = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

from dataclasses import dataclass
from typing import Optional, List, Tuple

@dataclass
class RedditContent:
    id: int
    source_id: str
    chunk_id: str
    type: str
    title: Optional[str]
    body: str
    subreddit: str
    permalink: str
    url: Optional[str]
    parent_id: Optional[str]
    created: float
    ups: Optional[int]
    downs: Optional[int]
    score: Optional[int]
    embedding: List[float]

@dataclass
class ScoredRedditContent:
    content: RedditContent
    similarity: float

def add_documents(content):
    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3096, chunk_overlap=128)
    chunks = text_splitter.split_text(content["body"])

    for i, chunk in enumerate(chunks):
        chunk_embedding = embedding_model.embed_query(chunk)
        chunk_id = f"{content['source_id']}_chunk_{i + 1}"

        sql = """
            INSERT INTO reddit_content (
                source_id, chunk_id, type, title, body, subreddit, permalink, url, parent_id, created, ups, downs, score, embedding
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s), %s, %s, %s, %s
            )
        """

        cursor.execute(sql, (
            content["source_id"],
            chunk_id,
            content["type"],
            content.get("title"),
            chunk,
            content["subreddit"],
            content["permalink"],
            content.get("url"),
            content.get("parent_id"),
            content["created"],  # This is now expected to be a Unix timestamp
            content.get("ups"),
            content.get("downs"),
            content.get("score"),
            chunk_embedding,
        ))

    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()

def ask(query) -> List[ScoredRedditContent]:
    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    query_embedding = embedding_model.embed_query(query)
    # Perform vector similarity search
    with conn.cursor() as cursor:
        sql = """
        SELECT *, 1 - (embedding <-> %s::vector) as similarity
        FROM reddit_content
        ORDER BY embedding <-> %s::vector
        LIMIT 5
        """
        cursor.execute(sql, (query_embedding, query_embedding))
        results = cursor.fetchall()

    # Convert tuple results to ScoredRedditContent objects
    return [ScoredRedditContent(RedditContent(*result[:-1]), result[-1]) for result in results]
