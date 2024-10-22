import os
from langchain_community.embeddings import OpenAIEmbeddings

OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)