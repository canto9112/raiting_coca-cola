from pprint import pprint
import requests
from dotenv import load_dotenv
import os
from itertools import count
import datetime
import time


def get_posts(ask, token, version_api, count_post, start_time, end_time):
    base_url = 'https://api.vk.com/method/newsfeed.search'
    all_posts = []

    for page in count(0, count_post):
        params = {
            'q': ask,
            'count': count_post,
            'access_token': token,
            'start_time': start_time,
            'end_time': end_time,
            'start_from': page,
            'v': version_api}
        page_response = requests.get(base_url, params=params)
        page_response.raise_for_status()
        page_data = page_response.json()
        if page >= page_data['response']['count']:
            break
        posts = page_data['response']['items']
        for post in posts:
            all_posts.append(post['text'])

    return len(all_posts)


def get_unix_timestamp(date):
    timestamp_day = datetime.datetime(year=date.year,
                                      month=date.month,
                                      day=date.day).timestamp()
    return int(timestamp_day)


if __name__ == "__main__":
    load_dotenv()

    service_token = os.getenv('VK_SERVICE_TOKEN')
    version_api = '5.126'
    count_post = 200
    start_time, end_time = 1613854800, 1613941200

    ask = 'Coca-Cola'
    today = datetime.date.today()
    timestamp_today = get_unix_timestamp(today)
    week = 7

    timestamp_last_week = []
    for day in range(1, week + 1):
        yesterday = today - datetime.timedelta(days=day)
        timestamp_yestarday = get_unix_timestamp(yesterday)

        posts_day = get_posts(ask, service_token, version_api,
                              count_post, timestamp_yestarday, timestamp_today)
        thistuple = tuple((yesterday, timestamp_yestarday, posts_day))
        timestamp_last_week.append(thistuple)
    pprint(timestamp_last_week)