import requests
import sys
from typing import List, Dict, Optional, Any
from reddit.cleaners.post import clean_reddit_object


def fetch_reddit_data(url: str) -> Optional[Dict]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
    return None

def fetch_reddit_new_posts(subreddit: str) -> Optional[Dict]:
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    data = fetch_reddit_data(url)
    return data['data']['children']

def fetch_reddit_search_posts(query: str, subreddit: Optional[str] = None) -> Optional[Dict]:
    # https://www.reddit.com/search.json?q=jobs
    # https://www.reddit.com/r/AI_Agents/search.json?q=jobs&restrict_sr=1

    if subreddit:
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1"   
    else:
        url = f"https://www.reddit.com/search.json?q={query}"
        
    data = fetch_reddit_data(url)
    return data['data']['children']
    
def fetch_and_clean_objects(url: str) -> Dict[str, Any]:
    json_url = url.rstrip('/') + '.json'
    post_data = fetch_reddit_data(json_url)
    
    if post_data:
        return clean_reddit_object(post_data)
    return []

def fetch_posts(urls: List[str]) -> List[Dict]:
    cleaned_posts = []
   
    for url in urls:
        cleaned_post = fetch_and_clean_objects(url)
        if cleaned_post:
            cleaned_posts.append({"post": cleaned_post[0], "comments": cleaned_post[1:]})
    
    return cleaned_posts