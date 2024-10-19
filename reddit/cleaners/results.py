from typing import List, Dict, Optional

def remove_posts_by_title(posts: List[Dict], exclude_phrases: List[str]) -> List[Dict]:
    """
    Remove posts whose titles contain any of the specified phrases (case-insensitive).
    """
    return [post for post in posts if not any(phrase.lower() in post['data']['title'].lower() for phrase in exclude_phrases)]

def remove_unanswered(posts: List[Dict]) -> List[Dict]:
    """
    Remove posts that contain a question mark in the title and have zero comments.
    """
    return [post for post in posts if not post['data']['num_comments'] == 0]

def remove_bad_posts(posts: List[Dict], remove_phrases: List[str] = None) -> List[Dict]:
    filtered_posts = remove_unanswered(posts)
    print(len(filtered_posts))
    print(remove_phrases)
    if remove_phrases:
        filtered_posts = remove_posts_by_title(filtered_posts, remove_phrases)
    print(len(filtered_posts))
    return filtered_posts