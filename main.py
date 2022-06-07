import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
BEARER = 'Bearer ' + ACCESS_TOKEN
API_URL = 'https://api-ssl.bitly.com/v4/{}'


def requests_get(url: str, get_param: str = '', headers: dict = None, params: dict = None) -> requests.Response:
    response = requests.get(url=url.format(get_param), headers=headers, params=params)
    response.raise_for_status()
    return response


def requests_post(url: str, get_param: str, headers: dict, payload: dict) -> requests.Response:
    response = requests.post(url=url.format(get_param), headers=headers, json=payload)
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
    requests_get(link)  # wrong long url test
    response = requests_post(API_URL, 'shorten', headers, payload)
    resp_json: dict = response.json()
    bitlink: str = resp_json['link']
    return bitlink


def count_clicks(link: str):
    headers = {
        'Authorization': BEARER,
    }
    params = {
        'units': '-1'
    }
    parsed = urlparse(link)
    parsed_bitlink = parsed.netloc + parsed.path
    api_method = 'bitlinks/' + parsed_bitlink + '/clicks/summary'
    response = requests_get(API_URL, api_method, headers, params)
    resp_json: dict = response.json()
    clicks = resp_json['total_clicks']
    return clicks


def print_shortened_link():
    user_info = retrieve_user_info()
    guid: str = user_info['default_group_guid']
    long_url = input('Введите ссылку: ')
    try:
        bitlink = shorten_link(long_url, guid)
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


def print_clicks_count():
    user_info = retrieve_user_info()
    guid: str = user_info['default_group_guid']
    long_url = 'https://gist.github.com/dvmn-tasks/58f5fdf7b8eb61ea4ed1b528b74d1ab5#Shorten'
    try:
        clicks = count_clicks(shorten_link(long_url, guid))
    except requests.exceptions.HTTPError as err:
        print('HTTP error:', err)
        print('It is possible that your link contains a typo.')
        exit(1)
    except Exception as e:
        print('Other error:', e)
        print("Please, contact script's author.")
        exit(1)
    else:
        print('Количество переходов:', clicks)


def is_bitlink() -> bool:
    pass


def choose_action() -> str:
    pass


def main():
    try:
        message = choose_action()
    except requests.exceptions.HTTPError as err:
        print('HTTP error:', err)
        print('It is possible that your link contains a typo.')
        exit(1)
    except Exception as e:
        print('Other error:', e)
        print("Please, contact script's author.")
        exit(1)
    else:
        print(message)


if __name__ == "__main__":
    print_clicks_count()
