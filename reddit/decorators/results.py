from typing import List, Dict
from llm import sentiment

def add_sentiment_scores(posts: List[Dict]) -> List[Dict]:
    for post in posts:
        title = post['post']['data']['children'][0]['data']['title']
        body = post['post']['data']['children'][0]['data']['selftext']
        sentiment_scores = sentiment.analyze(title +" "+ body)
        post['post']['data']['children'][0]['data']['sentiment_score'] = sentiment_scores['compound']
    return posts