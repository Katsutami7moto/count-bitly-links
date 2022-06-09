import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def retrieve_user_info() -> dict:
    headers = {
        'Authorization': BEARER,
    }
    api_method = 'user'
    response = requests.get(url=API_URL.format(api_method), headers=headers)
    response.raise_for_status()
    return response.json()


def shorten_link(link: str, group_guid: str) -> str:
    headers = {
        'Authorization': BEARER,
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly',
        'group_guid': group_guid,
    }
    api_method = 'shorten'
    response = requests.post(url=API_URL.format(api_method), headers=headers, json=payload)
    response.raise_for_status()
    resp_json: dict = response.json()
    bitlink: str = resp_json['link']
    return bitlink


def count_clicks(link: str) -> int:
    headers = {
        'Authorization': BEARER,
    }
    params = {
        'units': '-1'
    }
    parsed = urlparse(link)
    parsed_bitlink = parsed.netloc + parsed.path
    api_method = f'bitlinks/{parsed_bitlink}/clicks/summary'
    response = requests.get(url=API_URL.format(api_method), headers=headers, params=params)
    response.raise_for_status()
    clicks: int = response.json()['total_clicks']
    return clicks


def is_bitlink(link: str) -> bool:
    headers = {
        'Authorization': BEARER,
    }
    parsed = urlparse(link)
    parsed_bitlink = parsed.netloc + parsed.path
    api_method = f'bitlinks/{parsed_bitlink}'
    response = requests.get(url=API_URL.format(api_method), headers=headers)
    if response.ok:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception


def main():
    user_info = retrieve_user_info()
    guid: str = user_info['default_group_guid']
    while True:
        url = input('Enter a link (or just press "Enter" to quit): ')
        if not url:
            break
        try:
            if is_bitlink(url):
                message = f'Number of clicks: {count_clicks(url)}'
            else:
                message = f'Bitlink: {shorten_link(url, guid)}'
        except requests.exceptions.HTTPError as err:
            print('HTTP error:', err)
            print('It is possible that your link contains a typo.')
        except Exception as e:
            print('Other error:', e)
            print("If you don't know how to avoid this error, please, contact script's author.")
        else:
            print(message)
        finally:
            print()


if __name__ == "__main__":
    load_dotenv()
    ACCESS_TOKEN: str = os.getenv('ACCESS_TOKEN')
    BEARER = f'Bearer {ACCESS_TOKEN}'
    API_URL = 'https://api-ssl.bitly.com/v4/{}'
    main()
