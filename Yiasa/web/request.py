import requests

def get_request(url, timeout=3):
    try:
        return requests.get(url, timeout=timeout)
    except requests.exceptions.Timeout as timeout:
        raise requests.exceptions.Timeout(f'{url} timed out')
    except Exception as e:
        raise Exception(e)