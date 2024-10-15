import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any
import json
from reddit.requests import fetch_reddit_new_posts, fetch_reddit_data, filter_posts_by_date, remove_posts_by_title, remove_unanswered
from reddit.post import clean_reddit_object

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch posts from a specified subreddit for a given date")
    parser.add_argument("--timezone", default="UTC", help="Timezone name (e.g., America/New_York, Europe/London)")
    parser.add_argument("--subreddit", default="notebooklm", help="Subreddit name to fetch posts from")
    parser.add_argument("--date", help="Date to fetch posts for (YYYY-MM-DD). If not provided, uses current date in the specified timezone.")
    parser.add_argument("--remove", nargs='*', help="List of phrases to remove from post titles")
    return parser.parse_args()

def get_target_date(args: argparse.Namespace, tz: ZoneInfo) -> datetime:
    if args.date:
        return datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=tz)
    return datetime.now(tz)

def fetch_and_clean_post(url: str) -> Dict[str, Any]:
    json_url = url.rstrip('/') + '.json'
    post_data = fetch_reddit_data(json_url)
    if post_data:
        return clean_reddit_object(post_data)
    return {}

def process_posts(posts: List[Dict], target_date: datetime, tz: ZoneInfo, remove_phrases: List[str] = None) -> List[Dict]:
    filtered_posts = filter_posts_by_date(posts, target_date, tz)
    if remove_phrases:
        filtered_posts = remove_posts_by_title(filtered_posts, remove_phrases)
    filtered_posts = remove_unanswered(filtered_posts)
    
    cleaned_posts = []
    for post in filtered_posts:
        cleaned_post = fetch_and_clean_post(post['url'])
        if cleaned_post:
            cleaned_posts.append(cleaned_post)
    
    return cleaned_posts

def save_posts_to_json(posts: List[Dict], subreddit: str, date_str: str) -> None:
    filename = f"/data/{subreddit}_{date_str}.json"
    data = {
        "subreddit": subreddit,
        "date": date_str,
        "data": posts
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved posts to {filename}")

def main() -> None:
    args = parse_arguments()
    tz = ZoneInfo(args.timezone)
    target_date = get_target_date(args, tz)

    data = fetch_reddit_new_posts(args.subreddit)
    if data and 'data' in data and 'children' in data['data']:
        posts = data['data']['children']
        filtered_posts = process_posts(posts, target_date, tz, args.remove)
        date_str = target_date.strftime("%Y-%m-%d")
        
        if filtered_posts:
            save_posts_to_json(filtered_posts, args.subreddit, date_str)
            print(f"Processed and saved {len(filtered_posts)} posts for {date_str} in {args.timezone} from r/{args.subreddit}")
        else:
            print(f"No posts found for {date_str} in {args.timezone} from r/{args.subreddit}")
    else:
        print(f"No posts found or error occurred while fetching posts from r/{args.subreddit}")

if __name__ == "__main__":
    main()
