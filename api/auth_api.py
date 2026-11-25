class AuthApi:
    def __init__(self, client):
        self.client = client

    def register(self, credentials):
        return self.client.request('POST', '/signup', json_body=credentials.registration_payload())

    def login(self, credentials):
        return self.client.request('POST', '/signin', json_body=credentials.login_payload())
