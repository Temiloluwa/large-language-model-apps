import requests
import json 

def send_post_request(url, data, params=None):
    try:
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': response.status_code, 'body': response.text}
    except requests.exceptions.RequestException as e:
        return {'status': 'failed', 'body': f'Request failed {e}'}


def send_streaming_post_request(url, data, params=None):
    try:
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, params=params, headers=headers, stream=True)
        if response.status_code == 200:
            return response
        else:
            return {'status': response.status_code, 'body': response.text}
    except requests.exceptions.RequestException as e:
        return {'status': 'failed', 'body': f'Request failed: {e}'}