import requests

def get_request(url, timeout=3):
    try:
        req = requests.get(url, timeout=timeout)
        return req
    except requests.exceptions.Timeout as timeout:
        # TODO: log
        return None
    except Exception as e:
        # TODO: log
        return None