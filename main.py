from pprint import pprint
import requests
from dotenv import load_dotenv
import os


def get_first_page_posts(ask, token, version_api, posts_number,page_number):
    base_url = 'https://api.vk.com/method/newsfeed.search'
    params = {
        'q': ask,
        'count': posts_number,
        'access_token': token,
        'start_from': page_number,
        'v': version_api}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    response = response.json()
    first_page_posts = []
    for number in range(0, posts_number):
        response_text = response['response']['items'][number]['text']
        first_page_posts.append(response_text)
    return first_page_posts


def fetch_posts(page_number, ask, token, version_api, count_post):
    all_posts = []
    for page in range(1, page_number):
        posts = get_first_page_posts(ask, token, version_api, count_post, page)
        all_posts.extend(posts)
    return all_posts


if __name__ == "__main__":
    load_dotenv()

    service_token = os.getenv('VK_SERVICE_TOKEN')
    version_api = '5.126'
    count_post = 200
    page_number = 6

    ask = 'coca-cola'
    all_posts = fetch_posts(page_number, ask, service_token, version_api, count_post)
    print(len(all_posts))

