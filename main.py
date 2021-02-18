from pprint import pprint
import requests
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv('VK_SERVICE_TOKEN')
VERION_API = '5.126'

ask = 'Coca-Cola'

def fetch_json(ask, token, version_api):
    base_url = 'https://api.vk.com/method/newsfeed.search'
    params = {
        'q': ask,
        'count': 200,
        'access_token': token,
        'v': version_api}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


pprint(fetch_json(ask, TOKEN, VERION_API))

print('')