from storage.vector import ask, RedditContent, ScoredRedditContent
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ask.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    results = ask(query)
    for scored_content in results:
        print(f"Similarity: {scored_content.similarity:.4f}")
        content = scored_content.content
        print(f"ID: {content.id}")
        print(f"Source ID: {content.source_id}")
        print(f"Chunk ID: {content.chunk_id}")
        print(f"Type: {content.type}")
        print(f"Title: {content.title}")
        print(f"Body: {content.body}")
        print(f"Subreddit: {content.subreddit}")
        print(f"Permalink: {content.permalink}")
        print(f"URL: {content.url}")
        print(f"Parent ID: {content.parent_id}")
        print(f"Created: {content.created}")
        print(f"Ups: {content.ups}")
        print(f"Downs: {content.downs}")
        print(f"Score: {content.score}")
        print("---")  # Separator between results
