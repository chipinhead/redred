import requests
from datetime import datetime, timezone
import sys
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional

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
    return fetch_reddit_data(url)

def filter_posts_by_date(posts: List[Dict], target_date: datetime, tz: ZoneInfo) -> List[Dict]:
    filtered_posts = []
    for post in posts:
        created_utc = post['data']['created_utc']
        post_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).astimezone(tz).date()
        if post_date == target_date.date():
            filtered_posts.append(post['data'])
    return filtered_posts

def remove_posts_by_title(posts: List[Dict], exclude_text: str) -> List[Dict]:
    """
    Remove posts whose titles contain the specified text (case-insensitive).
    """
    return [post for post in posts if exclude_text.lower() not in post['title'].lower()]

def fetch_today_posts(subreddit: str = "notebooklm", tz_str: str = "UTC") -> List[Dict]:
    tz = ZoneInfo(tz_str)
    today = datetime.now(tz)

    data = fetch_reddit_new_posts(subreddit)
    if not data:
        return []

    try:
        posts = data['data']['children']
        return filter_posts_by_date(posts, today, tz)
    except KeyError as e:
        print(f"Error accessing post data: {e}", file=sys.stderr)
        return []
