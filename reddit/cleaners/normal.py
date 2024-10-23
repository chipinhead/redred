def check_required_keys(data):
    # Check if all required keys are present in the data
    required_keys = ['id', 'type', 'name', 'subreddit', 'permalink', 'created_utc']
    
    if not all(key in data for key in required_keys):
        print(f"Missing required keys: {required_keys}")
        return False
    
    # Additional checks for type-specific keys
    if data['type'] == 't3':  # Post
        if 'title' not in data or ('selftext' not in data and 'body' not in data):
            print(f"Missing title or body: {data['name']}")
            return False
    elif data['type'] == 't1':  # Comment
        if 'body' not in data or 'parent_id' not in data:   
            print(f"Missing body or parent_id: {data['name']}")
            return False
    # Check for either 'body' or 'selftext'
    if 'body' not in data and 'selftext' not in data:
        print(f"Missing body or selftext: {data['name']}")
        return False
    
    # Check for 'title' if it's a post
    if data.get("type") == "t3" and "title" not in data:
        print(f"Missing title: {data['name']}")
        return False

    return True

def normalize_reddit_data(data):
    if not check_required_keys(data):
        return None

    normalized = {
        "source_id": data.get("id"),
        "type": "post" if data.get("type") == "t3" else "comment" if data.get("type") == "t1" else "other",
        "name": data.get("name"),
        "title": data.get("title"),
        "body": data.get("body") or data.get("selftext"),
        "subreddit": data.get("subreddit"),
        "permalink": data.get("permalink"),
        "url": data.get("url"),
        "parent_id": data.get("parent_id"),
        "ups": data.get("ups"),
        "downs": data.get("downs"),
        "score": data.get("score"),
        "likes": data.get("likes"),
        "created": int(data.get("created_utc")),
    }

    return {k: v for k, v in normalized.items() if v is not None}