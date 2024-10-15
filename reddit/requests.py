import requests
from datetime import datetime, timezone
import sys
from zoneinfo import ZoneInfo

def fetch_today_posts(tz_str="UTC"):
    url = "https://www.reddit.com/r/notebooklm/new.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Get the current date in the specified timezone
        tz = ZoneInfo(tz_str)
        today = datetime.now(tz).date()

        today_posts = []
        for post in data['data']['children']:
            created_utc = post['data']['created_utc']
            # Convert UTC timestamp to the specified timezone
            post_date = datetime.fromtimestamp(created_utc, tz=timezone.utc).astimezone(tz).date()
            
            if post_date == today:
                today_posts.append(post['data'])

        return today_posts

    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
    except (KeyError, ValueError) as e:
        print(f"Error parsing data: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    
    return []
