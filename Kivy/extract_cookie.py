import requests


def convert_cookies_to_dict(cookie_jar):
    return requests.utils.dict_from_cookiejar(cookie_jar)