from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document, HumanMessage, AIMessage
from typing import List, Dict
from .db import get_vector_store, db_session
from llm.model import embedding
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from app.models import RedditContent
from datetime import datetime
import os



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

    vector_store = get_vector_store(os.environ.get("COLLECTION_NAME"))
    
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

def ask(query: str, conversation_history: List[Dict[str, str]] = None) -> str:
    vector_store = get_vector_store(os.environ.get("COLLECTION_NAME"))
    retriever = vector_store.as_retriever()
    llm = ChatOpenAI(model_name="gpt-4o-mini")

    # Create a system message for the prompt
    system_template = "Answer the user's question based only on the provided context and conversation history. Do not use any external knowledge."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Create a human message template for the context and query
    human_template = """Context: {context}

        Conversation history:
        {conversation_history}

        Current question: {input}

        Answer only based on the above context and conversation history:"""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combine the prompts
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Format the conversation history
    formatted_history = ""
    if conversation_history:
        for message in conversation_history:
            if message["role"] == "user":
                formatted_history += f"Human: {message['content']}\n"
            elif message["role"] == "assistant":
                formatted_history += f"AI: {message['content']}\n"

    # Create and invoke the chain
    combine_docs_chain = create_stuff_documents_chain(llm, chat_prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    response = retrieval_chain.invoke({
        "input": query,
        "conversation_history": formatted_history
    })

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
