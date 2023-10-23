import requests
import json 

def send_post_request(url, data, params=None):
    try:
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=data, params=params, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            print(f'Request failed with status code {response.status_code}')
            return {'status': response.status_code, 'body': response.text}
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return {'status': 'failed', 'body': 'Request failed'}


def send_streaming_post_request(url, data, params=None):
    try:
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=data, params=params, headers=headers, stream=True)
        if response.status_code == 200:
            return response
        else:
            print(f'Request failed with status code {response.status_code}')
            return {'status': response.status_code, 'body': response.text}
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return {'status': 'failed', 'body': 'Request failed'}