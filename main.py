import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def retrieve_user_info(bearer: str, api_url: str) -> dict:
    headers = {
        'Authorization': bearer,
    }
    api_method = 'user'
    response = requests.get(url=api_url.format(api_method), headers=headers)
    response.raise_for_status()
    return response.json()


def shorten_link(link: str, group_guid: str, bearer: str, api_url: str) -> str:
    headers = {
        'Authorization': bearer,
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly',
        'group_guid': group_guid,
    }
    api_method = 'shorten'
    response = requests.post(url=api_url.format(api_method), headers=headers, json=payload)
    response.raise_for_status()
    bitlink: str = response.json()['link']
    return bitlink


def count_clicks(link: str, bearer: str, api_url: str) -> int:
    headers = {
        'Authorization': bearer,
    }
    params = {
        'units': '-1'
    }
    parsed = urlparse(link)
    parsed_bitlink = f'{parsed.netloc}{parsed.path}'
    api_method = f'bitlinks/{parsed_bitlink}/clicks/summary'
    response = requests.get(url=api_url.format(api_method), headers=headers, params=params)
    response.raise_for_status()
    clicks: int = response.json()['total_clicks']
    return clicks


def is_bitlink(link: str, bearer: str, api_url: str) -> bool:
    headers = {
        'Authorization': bearer,
    }
    parsed = urlparse(link)
    parsed_bitlink = f'{parsed.netloc}{parsed.path}'
    api_method = f'bitlinks/{parsed_bitlink}'
    response = requests.get(url=api_url.format(api_method), headers=headers)
    return response.ok


def main():
    description = """
        Bitly URL shortener. 

        Console utility for shortening web links using bit.ly service and counting clicks on shortened links.
        """
    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument('-u', '--url', help='URL that you want to process')
    args = parser.parse_args()

    load_dotenv()
    access_token: str = os.getenv('ACCESS_TOKEN')
    bearer = f'Bearer {access_token}'
    api_url = 'https://api-ssl.bitly.com/v4/{}'
    guid: str = retrieve_user_info(bearer, api_url)['default_group_guid']

    while True:
        if args.url:
            url = args.url
        else:
            url = input('Enter a link (or just press "Enter" to quit): ')
        if not url:
            break
        try:
            wrong_url_test = requests.get(url)
            wrong_url_test.raise_for_status()
            if is_bitlink(url, bearer, api_url):
                message = f'Number of clicks: {count_clicks(url, bearer, api_url)}'
            else:
                message = f'Bitlink: {shorten_link(url, guid, bearer, api_url)}'
        except requests.exceptions.HTTPError as err:
            print('HTTP error:', err)
            print('It is possible that your link contains a typo.')
        except Exception as err:
            print('Other error:', err)
            print("If you don't know how to avoid this error, please, contact script's author.")
        else:
            print(message)
        finally:
            print()
            if args.url:
                break


if __name__ == "__main__":
    main()
