import requests
from dotenv import load_dotenv
import os
from itertools import count
import datetime
import plotly.graph_objects as go


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


def get_timestemp_last_week(ask, service_token, version_api, count_post, week):
    timestamp_last_week = []

    today = datetime.date.today()
    timestamp_today = get_unix_timestamp(today)

    for day in range(1, week + 1):
        yesterday = today - datetime.timedelta(days=day)
        timestamp_yestarday = get_unix_timestamp(yesterday)
        posts_day = get_posts(ask, service_token, version_api,
                              count_post, timestamp_yestarday, timestamp_today)
        thistuple = tuple((yesterday, posts_day))
        timestamp_last_week.append(thistuple)
    return timestamp_last_week


def get_graph(posts, ask):
    dates = []
    day_posts = []

    last_week_posts = list(posts)
    for day in last_week_posts:
        date = day[0]
        post = day[1]
        dates.append(date)
        day_posts.append(post)

    fig = go.Figure([go.Bar(x=dates, y=day_posts)])
    fig.update_layout(title_text=f'График упоминаний {ask} Вконтакте')
    fig.show()


if __name__ == "__main__":
    load_dotenv()

    service_token = os.getenv('VK_SERVICE_TOKEN')
    version_api = '5.126'
    count_post = 200
    week = 7
    ask = 'Coca-Cola'

    posts = get_timestemp_last_week(ask, service_token, version_api, count_post, week)
    get_graph(posts, ask)