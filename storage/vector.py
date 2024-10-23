from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
from .db import get_vector_store, db_session
from llm.model import embedding
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from app.models import RedditContent
from datetime import datetime



def add_documents(content: Dict):
    # Check if RedditContent with the same source_id already exists
    with db_session() as session:
        existing_content = session.query(RedditContent).filter(RedditContent.source_id == content["source_id"]).first()
        if existing_content:
            return False

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3096, chunk_overlap=128)
    chunks = text_splitter.split_text(content["body"])

    if content["type"] == "post":
        chunks.append(content["title"])

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
    try:
        if documents:
            vector_store.add_documents(documents)
    except Exception as e:
        print(f"Error adding documents to vector store: {e}")
        print("Documents:")
        for doc in documents:
            print(doc)
        return False
    

    # Log documents to the database
    log_documents(documents)

    return True

def ask(query: str) -> str:
    # Get the vector store
    vector_store = get_vector_store("reddit_content")
    
    # Create a retriever
    retriever = vector_store.as_retriever()

    # Create the language model with a specific model name
    llm = ChatOpenAI(model_name="gpt-4o-mini")

    # Create a prompt template
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    Context: {context}

    Question: {input}

    Answer: """)

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    
    # Invoke the chain
    response = retrieval_chain.invoke({"input": query})
    
    return response["answer"]

def log_documents(documents: List[Document]):
    with db_session() as session:
        for doc in documents:
            # Convert the 'created' timestamp to a datetime object
            created_datetime = datetime.fromtimestamp(doc.metadata["created"])
            
            content = RedditContent(
                source_id=doc.metadata["source_id"],
                chunk_id=doc.metadata["chunk_id"],
                type=doc.metadata["type"],
                title=doc.metadata.get("title"),
                body=doc.page_content,
                subreddit=doc.metadata["subreddit"],
                permalink=doc.metadata["permalink"],
                url=doc.metadata.get("url"),
                parent_id=doc.metadata.get("parent_id"),
                created=created_datetime,  # Use the converted datetime
                ups=doc.metadata.get("ups"),
                downs=doc.metadata.get("downs"),
                score=doc.metadata.get("score")
            )
            session.add(content)
