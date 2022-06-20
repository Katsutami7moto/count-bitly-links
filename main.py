import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def retrieve_user_info(bearer: str, api_base: str) -> dict:
    headers = {
        'Authorization': bearer,
    }
    api_method = 'user'
    api_url = api_base.format(api_method)
    response = requests.get(url=api_url, headers=headers)
    response.raise_for_status()
    return response.json()


def shorten_link(link: str, bearer: str, api_base: str) -> str:
    guid: str = retrieve_user_info(bearer, api_base)['default_group_guid']
    headers = {
        'Authorization': bearer,
    }
    payload = {
        'long_url': link,
        'domain': 'bit.ly',
        'group_guid': guid,
    }
    api_method = 'shorten'
    api_url = api_base.format(api_method)
    response = requests.post(url=api_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink: str = response.json()['link']
    return bitlink


def count_clicks(link: str, bearer: str, api_base: str) -> int:
    headers = {
        'Authorization': bearer,
    }
    params = {
        'units': '-1'
    }
    parsed = urlparse(link)
    parsed_bitlink = f'{parsed.netloc}{parsed.path}'
    api_method = f'bitlinks/{parsed_bitlink}/clicks/summary'
    api_url = api_base.format(api_method)
    response = requests.get(url=api_url, headers=headers, params=params)
    response.raise_for_status()
    clicks: int = response.json()['total_clicks']
    return clicks


def is_bitlink(link: str, bearer: str, api_base: str) -> bool:
    headers = {
        'Authorization': bearer,
    }
    parsed = urlparse(link)
    parsed_bitlink = f'{parsed.netloc}{parsed.path}'
    api_method = f'bitlinks/{parsed_bitlink}'
    api_url = api_base.format(api_method)
    response = requests.get(url=api_url, headers=headers)
    return response.ok


def main():
    description = """
        Bitly URL shortener. 
        Console utility for shortening web links using bit.ly service
        and counting clicks on shortened links.
        """
    parser = argparse.ArgumentParser(
        description=description
    )
    parser.add_argument('-u', '--url', help='URL that you want to process')
    args = parser.parse_args()

    load_dotenv()
    access_token: str = os.getenv('ACCESS_TOKEN')
    bearer = f'Bearer {access_token}'
    api_base = 'https://api-ssl.bitly.com/v4/{}'

    while True:
        if args.url:
            user_url: str = args.url
        else:
            user_url = input('Enter a link (or press "Enter" to quit): ')
        if not user_url:
            break
        user_url = user_url.strip()
        try:
            requests.get(user_url).raise_for_status()
            api_args = user_url, bearer, api_base
            if is_bitlink(*api_args):
                message = f'Number of clicks: {count_clicks(*api_args)}'
            else:
                message = f'Bitlink: {shorten_link(*api_args)}'
        except requests.exceptions.HTTPError as err:
            print('HTTP error:', err)
            print('It is possible that your link contains a typo.')
        except Exception as err:
            print('Other error:', err)
            print("""If you don't know how to avoid this error,\
            please, contact script's author.""")
        else:
            print(message)
        finally:
            print()
            if args.url:
                break


if __name__ == "__main__":
    main()
