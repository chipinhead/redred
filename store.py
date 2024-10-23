import json
import sys
from reddit.cleaners.normal import normalize_reddit_data
from storage.vector import add_documents

def process_reddit_data(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    posts = []
    # Process each object in the JSON array
    for item in data:
        # Normalize the data
        normalized_data = normalize_reddit_data(item)
        if not normalized_data:
            continue

        # Add the normalized data to the vector store
        result = add_documents(normalized_data)

        if result and normalized_data["type"] == "post":
            posts.append(normalized_data)

    print(f"Processed {len(data)} items from {json_file_path}")
    return posts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_reddit_data.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    posts = process_reddit_data(json_file_path)
    for post in posts:
        print(f"Post {post['source_id']}: {post['title']}")
