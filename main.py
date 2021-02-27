import datetime
import os

import plotly.graph_objects as go
import requests
from dotenv import load_dotenv


def fetch_number_posts_per_day(url, query, token, version_api, start_time, end_time):
    params = {
        'q': query,
        'access_token': token,
        'start_time': start_time,
        'end_time': end_time,
        'v': version_api}
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    return response['response']['total_count']


def get_unix_timestamp(date):
    timestamp_day = datetime.datetime(year=date.year,
                                      month=date.month,
                                      day=date.day).timestamp()
    return int(timestamp_day)


def get_timestemp_past_days(days):
    timestamp_past_days = []
    today = datetime.date.today()
    for day in range(1, days):
        start_day = today - datetime.timedelta(days=day)
        end_day = start_day + datetime.timedelta(days=1)
        timestamp_start_day = get_unix_timestamp(start_day)
        timestamp_end_day = get_unix_timestamp(end_day)
        timestamp_past_days.append((start_day, timestamp_start_day, timestamp_end_day))
    return timestamp_past_days


def get_all_posts(days, base_url, search_query, service_token, version_api):
    timestemp_past_days = get_timestemp_past_days(days)
    all_posts = []
    for start_day, timestamp_start_day, timestamp_end_day in timestemp_past_days:
        per_day_posts = fetch_number_posts_per_day(base_url, search_query, service_token,
                                                   version_api, timestamp_start_day, timestamp_end_day)
        all_posts.append((start_day, per_day_posts))
    return all_posts


def get_graph(posts, ask, days):
    dates = []
    day_posts = []

    last_week_posts = list(posts)
    for date, post in last_week_posts:
        dates.append(date)
        day_posts.append(post)

    fig = go.Figure([go.Bar(x=dates, y=day_posts)])
    fig.update_layout(title_text=f'График упоминаний {ask} за {days} дней Вконтакте')
    fig.show()


def main():
    load_dotenv()

    service_token = os.getenv('VK_SERVICE_TOKEN')

    base_url = 'https://api.vk.com/method/newsfeed.search'
    version_api = '5.126'
    search_query = 'Coca-Cola'
    days = 7

    all_posts = get_all_posts(days, base_url, search_query, service_token, version_api)

    get_graph(all_posts, search_query, days)


if __name__ == "__main__":
    main()
