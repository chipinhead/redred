def normalize_reddit_data(data):
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