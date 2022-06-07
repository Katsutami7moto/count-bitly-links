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


def requests_get(url: str, get_param: str, headers: dict) -> requests.Response:
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
        exit(1)
    except Exception as e:
        print('Other error', e)
        exit(1)
    else:
        print('Битлинк:', bitlink)


if __name__ == "__main__":
    print_shortened_link()

# Wrong long url POST response.text:
# {
#     "created_at": "2022-06-07T09:04:05+0000",
#     "id": "bit.ly/3Ntmiqz",
#     "link": "https://bit.ly/3Ntmiqz",
#     "custom_bitlinks": [],
#     "long_url": "https://stackoverflow.com/question/16511337",
#     "archived": false,
#     "tags": [],
#     "deeplinks": [],
#     "references": {
#         "group": "https://api-ssl.bitly.com/v4/groups/Bm66bEvGrH0"
#     }
# }
# Right long url POST response.text:
# {
#     "created_at": "2022-06-07T09:07:04+0000",
#     "id": "bit.ly/3Q15uc2",
#     "link": "https://bit.ly/3Q15uc2",
#     "custom_bitlinks": [],
#     "long_url": "https://stackoverflow.com/questions/16511337",
#     "archived": false,
#     "tags": [],
#      "deeplinks": [],
#     "references": {
#         "group": "https://api-ssl.bitly.com/v4/groups/Bm66bEvGrH0"
#     }
# }
