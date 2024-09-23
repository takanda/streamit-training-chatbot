import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv


load_dotenv()


class QiitaClient():
    
    def __init__(self):
        current_date = date.today()
        one_month_ago = current_date - timedelta(days=30)
        self.url = f"https://qiita.com/api/v2/items?page=1&per_page=50&query=created:>{one_month_ago}+stocks:>20"
        self.headers = {
            "Authorization": f"Bearer {os.environ['QIITA_API_KEY']}"
        }
        
    def get_trending_articles(self):
        response = requests.get(url=self.url, headers=self.headers)
        response.raise_for_status()
        result = response.json()
        
        trending_articles = []
        for res in result:
            trending_articles.append({
                "title":        res["title"],
                "tag":          [tag["name"] for tag in res["tags"]],
                "url":          res["url"],
                "likes_count":  res["likes_count"],
                "stocks_count": res["stocks_count"]
            })
        
        print(f"trending_articles> {trending_articles}")
        return trending_articles
    