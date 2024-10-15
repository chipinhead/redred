import requests
from datetime import datetime, timezone
import sys

def fetch_today_posts():
    url = "https://www.reddit.com/r/notebooklm/new.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        today = datetime.now(timezone.utc).date()

        print("Posts created today:")
        for post in data['data']['children']:
            created_utc = post['data']['created_utc']
            post_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).date()
            
            if post_date == today:
                print(f"- {post['data']['title']}")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
    except (KeyError, ValueError) as e:
        print(f"Error parsing data: {e}", file=sys.stderr)

if __name__ == "__main__":
    fetch_today_posts()
