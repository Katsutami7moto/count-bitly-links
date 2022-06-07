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


def requests_get(url: str, get_param: str = '', headers: dict = None) -> requests.Response:
    response = requests.get(url=url.format(get_param), headers=headers)
    response.raise_for_status()
    return response


def requests_post(url: str, get_param: str, headers: dict, payload: dict) -> requests.Response:
    response = requests.post(url=url.format(get_param), headers=headers, json=payload)
    status = response.status_code
    print('Status code', status)
    print('Response text:', response.text)
    response.raise_for_status()
    return response


def retrieve_user_info() -> dict:
    headers = {
        'Authorization': BEARER,
    }
    response = requests_get(API_URL, 'user', headers)
    return response.json()


def shorten_link(link: str, group_guid: str) -> str:
    headers = {
        'Authorization': BEARER,
        'Content-Type': 'application/json',
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly',
        'group_guid': group_guid,
    }
    long_url_test = requests_get(link)
    long_url_test.raise_for_status()
    response = requests_post(API_URL, 'shorten', headers, payload)
    resp_json: dict = response.json()
    bitlink: str = resp_json['link']
    return bitlink


def print_shortened_link():
    user_info = retrieve_user_info()
    guid: str = user_info['default_group_guid']
    url_to_shorten = input('Введите ссылку: ')
    try:
        bitlink = shorten_link(url_to_shorten, guid)
    except requests.exceptions.HTTPError as err:
        print('HTTP error:', err)
        print('It is possible that your link contains a typo.')
        exit(1)
    except Exception as e:
        print('Other error:', e)
        print("Please, contact script's author.")
        exit(1)
    else:
        print('Битлинк:', bitlink)


if __name__ == "__main__":
    print_shortened_link()
