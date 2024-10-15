import argparse
from reddit.requests import fetch_today_posts

def main():
    parser = argparse.ArgumentParser(description="Fetch today's posts from a specified subreddit")
    parser.add_argument("--timezone", default="UTC", help="Timezone name (e.g., America/New_York, Europe/London)")
    parser.add_argument("--subreddit", default="notebooklm", help="Subreddit name to fetch posts from")
    args = parser.parse_args()

    posts = fetch_today_posts(subreddit=args.subreddit, tz_str=args.timezone)
    
    print(f"Posts created today in {args.timezone} from r/{args.subreddit}:")
    for post in posts:
        print(f"- {post['title']}")
        print(f"  Author: {post['author']}")
        print(f"  URL: {post['url']}")
        print(f"  Score: {post['score']}")
        print()

if __name__ == "__main__":
    main()
