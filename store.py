import json
import sys
from reddit.cleaners.normal import normalize_reddit_data
from storage.vector import add_documents

def process_reddit_data(json_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Process each object in the JSON array
    for item in data:
        # Normalize the data
        normalized_data = normalize_reddit_data(item)

        # Add the normalized data to the vector store
        add_documents(normalized_data)

    print(f"Processed {len(data)} items from {json_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_reddit_data.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    process_reddit_data(json_file_path)
