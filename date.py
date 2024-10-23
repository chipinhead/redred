import argparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import List, Dict, Any
import json
from reddit.requests import fetch_reddit_new_posts, fetch_posts
from reddit.cleaners.results import remove_bad_posts

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

def filter_posts_by_date(posts: List[Dict], target_date: datetime, tz: ZoneInfo) -> List[Dict]:
    filtered_posts = []
    for post in posts:
        created_utc = post['data']['created_utc']
        post_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).astimezone(tz).date()
        if post_date == target_date.date():
            filtered_posts.append(post)
    return filtered_posts

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
    posts = fetch_reddit_new_posts(args.subreddit)
    print(f"{len(posts)} posts found")
    posts = remove_bad_posts(posts, args.remove)
    print(f"{len(posts)} remaining after removing bad posts")
    posts = filter_posts_by_date(posts, target_date, tz)
    print(f"{len(posts)} were posted on {target_date.strftime('%Y-%m-%d')}")
    posts = fetch_posts([post['data']['url'] for post in posts if post['data']['url'].endswith('/')])
    date_str = target_date.strftime("%Y-%m-%d")
    
    if posts:
        save_posts_to_json(posts, args.subreddit, date_str)
        print(f"Processed and saved {len(posts)} posts for {date_str} in {args.timezone} from r/{args.subreddit}")
    else:
        print(f"No posts found for {date_str} in {args.timezone} from r/{args.subreddit}")

if __name__ == "__main__":
    main()
