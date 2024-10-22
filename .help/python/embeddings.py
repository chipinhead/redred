from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import psycopg2
from datetime import datetime

# Initialize embedding model and text splitter
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key="YOUR_API_KEY")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# Example connection setup to PostgreSQL
connection_string = "postgresql://user:password@localhost:5432/mydatabase"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

# Example content (can be post or comment) with Unix timestamp
content = {
    "source_id": "t3_1g8x6hy",  # Unique ID from the source (e.g., Reddit)
    "type": "post",  # Can be "post" or "comment"
    "name": "t3_1g8x6hy",  # Name of the content
    "title": "Openai advanced audio feature alternatives",  # Only applicable for posts
    "body": "Is there any alternatives of Chatgpt advanced voice mode... (long content here)",  # The actual content
    "created": 1729535939.0,  # Unix timestamp (seconds since epoch)
    "ups": 2,  # Upvotes
    "downs": 0,  # Downvotes
    "score": 2,  # Score
    "subreddit": "OpenAI",  # Subreddit where it was posted
    "permalink": "/r/OpenAI/comments/1g8x6hy/openai_advanced_audio_feature_alternatives/",
    "url": "https://www.reddit.com/r/OpenAI/comments/1g8x6hy/openai_advanced_audio_feature_alternatives/"
}

# Convert Unix timestamp to datetime format for PostgreSQL
created_datetime = datetime.utcfromtimestamp(content["created"])

# Chunk the content body
chunks = text_splitter.split_text(content["body"])

# Insert each chunk into the database with its embedding
for i, chunk in enumerate(chunks):
    chunk_embedding = embedding_model.embed_query(chunk)
    chunk_name = f"{content['source_id']}_chunk_{i + 1}"  # Create a unique name for each chunk

    # Inserting into the content table with an auto-increment "id", "source_id", and "source"
    sql = """
        INSERT INTO content (
            source_id, name, type, title, body, subreddit, permalink, url, parent_id, created, ups, downs, score, embedding, source
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    cursor.execute(sql, (
        content["source_id"],  # Original ID from Reddit
        chunk_name,  # Unique name for each chunk
        content["type"],  # "post" or "comment"
        content.get("title"),  # Title (if applicable, can be None for comments)
        chunk,  # Insert the chunk instead of the full body
        content["subreddit"],
        content["permalink"],
        content.get("url"),
        content.get("source_id"),  # Use the original content's source_id as parent_id
        created_datetime,  # Use the converted timestamp
        content.get("ups"),
        content.get("downs"),
        content.get("score"),
        chunk_embedding,
        "reddit"  # Set "source" to "reddit"
    ))

# Commit changes
conn.commit()

############

query = "Are there any alternatives to ChatGPT's voice feature?"
query_embedding = embedding_model.embed_query(query)

# Perform vector similarity search
sql = """
    SELECT * FROM content WHERE embedding <-> %s LIMIT 5
"""
cursor.execute(sql, (query_embedding,))
results = cursor.fetchall()

for result in results:
    print(result)  # This will print the relevant post/comment records