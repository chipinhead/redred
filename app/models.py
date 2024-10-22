from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base

# Define the base for your models
Base = declarative_base()

# Define your Content model
class RedditContent(Base):
    __tablename__ = 'reddit_contents'
    
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