import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BEARER = 'Bearer {TOKEN}'.format(TOKEN=ACCESS_TOKEN)
API_URL = 'https://api-ssl.bitly.com/v4/{}'


def json_pretty_print(response: dict):
    print(json.dumps(response, indent=4, ensure_ascii=False))


def requests_get(url: str, get_param: str, headers: dict[str, str]) -> requests.Response:
    response = requests.get(url=url.format(get_param), headers=headers)
    response.raise_for_status()
    return response


def requests_post(url: str, get_param: str, headers: dict[str, str], payload: dict[str, str]) -> requests.Response:
    response = requests.post(url=url.format(get_param), headers=headers, json=payload)
    response.raise_for_status()
    return response


def retrieve_user_info() -> dict:
    headers = {
        'Authorization': BEARER,
    }
    response = requests_get(API_URL, 'user', headers)
    return response.json()


def shorten_link(link: str, group_guid: str) -> dict:
    headers = {
        'Authorization': BEARER,
        'Content-Type': 'application/json',
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly',
        'group_guid': group_guid,
    }
    response = requests_post(API_URL, 'shorten', headers, payload)
    return response.json()


def print_shortened_link():
    user_info = retrieve_user_info()
    guid: str = user_info['default_group_guid']
    url_to_shorten = input('Введите ссылку: ')
    shortened_link = shorten_link(url_to_shorten, guid)
    print('Битлинк:', shortened_link['link'])


if __name__ == "__main__":
    print_shortened_link()
