from typing import Dict, Any

def clean_reddit_object(obj: Dict[str, Any]) -> Dict[str, Any]:
    allowed_keys = ["kind", "data", "children", "selftext", "title", "created_utc", "created", "likes", "replies", "body", "score", "ups", "downs", "url", "permalink"]
    
    if isinstance(obj, dict):
        return {k: clean_reddit_object(v) for k, v in obj.items() if k in allowed_keys}
    elif isinstance(obj, list):
        return [clean_reddit_object(item) for item in obj]
    else:
        return obj
