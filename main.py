import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def json_pretty_print(response):
    print(json.dumps(response, indent=4, ensure_ascii=False))


def requests_get(url: str, get_param: str, headers: dict, params: dict = None) -> requests.Response:
    response = requests.get(url=url.format(get_param), params=params, headers=headers)
    response.raise_for_status()
    return response


def main():
    headers = {
        'Authorization': 'Bearer {TOKEN}'.format(TOKEN=ACCESS_TOKEN),
    }
    bitly_api_url = 'https://api-ssl.bitly.com/{}'
    to_retrieve_user = 'v4/user'
    response = requests_get(bitly_api_url, to_retrieve_user, headers)
    json_pretty_print(response.json())


if __name__ == "__main__":
    main()
