import argparse
from typing import List, Dict, Any, Optional
from reddit.requests import fetch_reddit_search_posts, fetch_posts
from reddit.cleaners.results import remove_bad_posts
import json
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search Reddit for posts matching a given phrase")
    parser.add_argument("query", help="Query to search for")
    parser.add_argument("--subreddit", help="Optional Subreddit name to fetch posts from")
    parser.add_argument("--remove", nargs='*', help="List of phrases to remove from post titles")
    return parser.parse_args()

def save_posts_to_json(posts: List[Dict], query: str, subreddit: Optional[str] = None) -> None:
    if subreddit:
        filename = f"/data/{subreddit}_{query}.json"
    else:
        filename = f"/data/{query}.json"

    data = {
        "query": query,
        "data": posts
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved posts to {filename}")

def main() -> None:
    args = parse_arguments()
    posts = fetch_reddit_search_posts(args.query, args.subreddit)
    print(f"{len(posts)} posts found")
    remaining = remove_bad_posts(posts, args.remove)
    print(f"{len(remaining)} remaining after removing bad posts")
    posts = fetch_posts([post['data']['url'] for post in remaining])
    
    if posts:
        save_posts_to_json(posts, args.query, args.subreddit)
        for post in remaining:
            print(post['data']['title'])
        print(f"Processed and saved {len(posts)}")
    else:
        print(f"No posts found")

if __name__ == "__main__":
    main()
