from pprint import pprint
import requests
from dotenv import load_dotenv
import os
from itertools import count
import datetime


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

    print(len(all_posts))


if __name__ == "__main__":
    load_dotenv()

    service_token = os.getenv('VK_SERVICE_TOKEN')
    version_api = '5.126'
    count_post = 200
    start_time, end_time = 1613854800, 1613941200

    ask = 'Coca-Cola'

    get_posts(ask, service_token, version_api,
              count_post, start_time, end_time)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print(yesterday)

