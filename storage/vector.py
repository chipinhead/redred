from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
from .db import get_vector_store
from llm.model import embedding

def add_documents(content: Dict):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3096, chunk_overlap=128)
    chunks = text_splitter.split_text(content["body"])

    documents = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"{content['source_id']}_chunk_{i + 1}"
        doc = Document(
            page_content=chunk,
            metadata={
                "source_id": content["source_id"],
                "chunk_id": chunk_id,
                "type": content["type"],
                "title": content.get("title"),
                "body": chunk,
                "subreddit": content["subreddit"],
                "permalink": content["permalink"],
                "url": content.get("url"),
                "parent_id": content.get("parent_id"),
                "created": content["created"],
                "ups": content.get("ups"),
                "downs": content.get("downs"),
                "score": content.get("score"),
            }
        )
        
        documents.append(doc)

    vector_store = get_vector_store("reddit_content")
    
    # Add documents to the vector store
    vector_store.add_documents(documents)

def ask(query: str) -> List[Dict]:
    vector_store = get_vector_store("reddit_content")
    results = vector_store.similarity_search_with_score(query, k=5)
    
    return [
        {
            "content": result[0].page_content,
            "metadata": result[0].metadata,
            "similarity": result[1]
        }
        for result in results
    ]
