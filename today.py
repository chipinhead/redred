import argparse
from reddit.requests import fetch_today_posts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch today's posts from r/notebooklm")
    parser.add_argument("--timezone", default="UTC", help="Three-letter timezone code (e.g., PST, EST)")
    args = parser.parse_args()

    posts = fetch_today_posts(args.timezone)
    
    print(f"Posts created today in {args.timezone}:")
    for post in posts:
        print(f"- {post['title']}")
        print(f"  Author: {post['author']}")
        print(f"  URL: {post['url']}")
        print(f"  Score: {post['score']}")
        print()
