import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict
from reddit.requests import fetch_reddit_new_posts, filter_posts_by_date, remove_posts_by_title, remove_unanswered

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch posts from a specified subreddit for a given date")
    parser.add_argument("--timezone", default="UTC", help="Timezone name (e.g., America/New_York, Europe/London)")
    parser.add_argument("--subreddit", default="notebooklm", help="Subreddit name to fetch posts from")
    parser.add_argument("--date", help="Date to fetch posts for (YYYY-MM-DD). If not provided, uses current date in the specified timezone.")
    return parser.parse_args()

def get_target_date(args: argparse.Namespace, tz: ZoneInfo) -> datetime:
    if args.date:
        return datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=tz)
    return datetime.now(tz)

def process_posts(posts: List[Dict], target_date: datetime, tz: ZoneInfo) -> List[Dict]:
    filtered_posts = filter_posts_by_date(posts, target_date, tz)
    filtered_posts = remove_posts_by_title(filtered_posts, "deep dive")
    return remove_unanswered(filtered_posts)

def print_posts(filtered_posts: List[Dict], date_str: str, timezone: str, subreddit: str) -> None:
    print(f"Posts for {date_str} in {timezone} from r/{subreddit} (excluding 'deep dive' posts and unanswered questions):")
    for post in filtered_posts:
        print(f"- {post['title']}")
        print(f"  Author: {post['author']}")
        print(f"  URL: {post['url']}")
        print(f"  Score: {post['score']}")
        print(f"  Comments: {post['num_comments']}")
        print()

def main() -> None:
    args = parse_arguments()
    tz = ZoneInfo(args.timezone)
    target_date = get_target_date(args, tz)

    data = fetch_reddit_new_posts(args.subreddit)
    if data and 'data' in data and 'children' in data['data']:
        posts = data['data']['children']
        filtered_posts = process_posts(posts, target_date, tz)
        date_str = target_date.strftime("%Y-%m-%d")
        print_posts(filtered_posts, date_str, args.timezone, args.subreddit)
    else:
        print(f"No posts found or error occurred while fetching posts from r/{args.subreddit}")

if __name__ == "__main__":
    main()
