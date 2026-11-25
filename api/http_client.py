import allure
import requests

from config import API_URL, REQUEST_TIMEOUT
from helpers.reporting import attach_json


class HttpClient:
    def __init__(self):
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def request(self, method, path, token=None, json_body=None, form=None):
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        files = {key: (None, str(value)) for key, value in form.items()} if form is not None else None
        with allure.step(f'{method} {path}'):
            attach_json('Запрос', {
                'method': method,
                'url': API_URL + path,
                'headers': headers,
                'content_type': 'multipart/form-data' if form is not None else 'application/json' if json_body is not None else None,
                'body': form if form is not None else json_body,
            })
            response = self.session.request(
                method, API_URL + path, headers=headers, json=json_body,
                files=files, timeout=REQUEST_TIMEOUT,
            )
            try:
                body = response.json()
            except ValueError:
                body = response.text
            attach_json('Ответ', {'status_code': response.status_code, 'body': body})
            return response
